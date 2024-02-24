from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from django.utils.crypto import get_random_string
from django.db import models
from django.utils import timezone
from django.core.mail import EmailMessage, get_connection

class Job(models.Model):
    profesion_CHOICES = [
        ('limpieza', 'Limpiador/a'),
        ('reparacion', 'Reparador/a'),
        ('jardineria', 'Jardinero/a'),
        ('electricista', 'Electricista'),
        ('fontanero', 'Fontanero/a'),
        ('carpintero', 'Carpintero/a'),
        ('pintor', 'Pintor/a'),
        ('albanil', 'Albañil'),
        ('cerrajero', 'Cerrajero/a'),
        ('podador_arboles', 'Podador/a de árboles'),
        ('disenador_jardines', 'Diseñador/a de jardines'),
        ('conductor_mudanzas', 'Conductor/a de mudanzas'),
        ('ayudante_mudanzas', 'Ayudante de mudanzas'),
        ('mensajero', 'Mensajero/a'),
        ('repartidor_alimentos', 'Repartidor/a de alimentos'),
        ('repartidor_paquetes', 'Repartidor/a de paquetes'),
        ('ninera', 'Niñera'),
        ('cuidador_personas_mayores', 'Cuidador/a de personas mayores'),
        ('asistente_personal', 'Asistente/a personal'),
        ('montador_muebles', 'Montador/a de muebles'),
        ('desmontador_muebles', 'Desmontador/a de muebles'),
        ('reparador_computadoras', 'Reparador/a de computadoras'),
        ('tecnico_electronica', 'Técnico/a en electrónica'),
        ('instalador_seguridad', 'Instalador/a de sistemas de seguridad'),
        ('disenador_grafico', 'Diseñador/a gráfico/a'),
        ('ilustrador', 'Ilustrador/a'),
        ('fotografo', 'Fotógrafo/a'),
        ('entrenador_personal', 'Entrenador/a personal'),
        ('instructor_yoga', 'Instructor/a de yoga'),
        ('preparador_fisico', 'Preparador/a físico/a'),
        ('organizador_eventos', 'Organizador/a de eventos'),
        ('animador', 'Animador/a'),
        ('dj', 'DJ'),
        ('asistente_administrativo', 'Asistente/a administrativo/a'),
        ('secretario', 'Secretario/a'),
        ('data_entry', 'Data Entry'),
        ]

    job = models.CharField(max_length=100, choices=profesion_CHOICES)


    def __str__(self):
        return self.job
    
class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) #campo heredado de user
    nombre = models.CharField(max_length=100, blank=True, editable=False)#campo heredado de user
    apellido = models.CharField(max_length=60, blank=True, editable=False)#campo heredado de user
    email = models.CharField(max_length=100, blank=True, editable=False)#campo heredado de user
    foto_perfil = models.ImageField(null=True, blank=True)
    ciudad = models.CharField(max_length=65)
    provincia = models.CharField(max_length=65)
    edad = models.IntegerField(null=True, blank=True)

    sexo_CHOICES = [
            ('H', 'Hombre'),
            ('M', 'Mujer'),
        ]

    sexo = models.CharField(max_length=20, choices=sexo_CHOICES)
    job = models.ManyToManyField(Job, related_name="usuarios_trabajo", blank=True)  # Eliminé null=True

    last_login = models.DateTimeField(blank=True, null=True)
    first_login = models.DateTimeField(blank=True, null=True)

    # codigo nuevo
    password_reset_token = models.CharField(max_length=32, blank=True, null=True)
    password_reset_token_created_at = models.DateTimeField(blank=True, null=True)


    def _reset_token_null(self):
        anterior_token = self.password_reset_token
        self.password_reset_token = "token_eliminado"
        self.password_reset_token_created_at = None
        self.save()
        return(f"el token era: {anterior_token} y ahora es: {self.password_reset_token}")
    
    def show_token_password(self):
        return (self.password_reset_token)

    def _generate_and_send_token(self):
        token = get_random_string(length=32)
        self.password_reset_token = token
        self.password_reset_token_created_at = timezone.now()
        self.save()

        reset_url = f"http://localhost:8000/reset_password/{token}/"
        emailw = EmailMessage(
            "Hello",
            f"URL: {reset_url}",
            "frankoocarp22@gmail.com",
            [self.user.email]
        ).send(fail_silently=False)
        
        return token
    # codigo nuevo
    
    def __str__(self):
        return (self.user.username)  

    def save(self, *args, **kwargs):
        if not self.nombre:
            self.nombre = self.user.first_name
        
        if not self.apellido:
            self.apellido = self.user.last_name
        
        if not self.email:
            self.email = self.user.email
        
        if not self.first_login:
            self.first_login = self.user.date_joined - timedelta(hours=3)

        super().save(*args, **kwargs)



class Empleo(models.Model):
    oferente = models.ForeignKey("Oferente", on_delete=models.CASCADE)
    titulo = models.CharField(max_length=50, blank=True, null=True)
    barrio = models.CharField(max_length=50, blank=True, null=True)
    ciudad = models.CharField(max_length=50, blank=True, null=True)
    provincia = models.CharField(max_length=50, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)  # Se establecerá automáticamente al crear la instancia
    modalidad_trabajo = [
        ('por hora de trabajo', 'por hora de trabajo'),
        ('por trabajo completo', 'por trabajo completo'),
        ('A convenir', "A convenir")
    ]
    trabajo = models.CharField(max_length=100, choices=modalidad_trabajo, blank=True, null=True)
    oferta = models.IntegerField(blank=True, null=True)
    descripcion = models.CharField(max_length=500)
    imagen_trabajo = models.ImageField(null=True, blank=True)
    vigente = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # Suma 3 horas al tiempo actual antes de guardar
        self.fecha_creacion = timezone.now() + timezone.timedelta(hours=3)
        super().save(*args, **kwargs)

    def return_oferente(self):
        return self.oferente
    
    def set_vigente(self):
        self.vigente = False
        self.save()  
    

class Oferente(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    prob_jugo = models.FloatField(blank=True, null=True)
    nro_transacciones = models.IntegerField(default=0)
    nro_transacciones_ofertadas = models.IntegerField(default=0)
    seriedad = models.FloatField(blank=True, null=True)  # Cambio de __seriedad a seriedad

    def realizar_transaccion(self, ofrece_jugo: float, ofrece_tips: float):
        self.nro_transacciones += 1

        # Evitar división por cero
        if self.nro_transacciones != 0:
            self.prob_jugo = (self.prob_jugo + ofrece_jugo) / self.nro_transacciones
            self.prob_tips = (self.prob_tips + ofrece_tips) / self.nro_transacciones

        self.save()
    
    

    # def calcular_seriedad(self):
    #     # Evitar división por cero
    #     if self.nro_transacciones != 0:
    #         self.seriedad = 0.1 * self.prob_jugo + 0.1 * self.prob_tips + 0.9 * (self.nro_transacciones_ofertadas / self.nro_transacciones)
    #         return self.seriedad
    #     else:
    #         return "Aún no se realizan transacciones"  # Manejar caso de nro_transacciones igual a cero

# DEFINIR FUNCIONES PARA ACTUALIZAR SERIEDAD Y PROP TOKENS EN BASE A PUNTUACIÓN DE LOS USUARIOS. 

class Trabajador(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    habilidades = models.ManyToManyField('Job', related_name='trabajadores_habilidad', blank=True)
    experiencia = models.TextField(blank=True, null=True)
    calificaciones = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.usuario.user.username

    def set_calificacion(self, nueva_calificacion):
        if self.calificaciones is None:
            # Si no hay calificaciones anteriores, establece la nueva calificación directamente
            self.calificaciones = nueva_calificacion
        else:
            # Calcula la nueva calificación media
            numero_calificaciones = self.usuario.nro_transacciones  # Puedes ajustar esto según la lógica de tu aplicación
            suma_calificaciones = self.calificaciones * numero_calificaciones
            nueva_suma_calificaciones = suma_calificaciones + nueva_calificacion
            nuevo_numero_calificaciones = numero_calificaciones + 1
            self.calificaciones = nueva_suma_calificaciones / nuevo_numero_calificaciones

        self.save()

"""
Esta clase crea una instancia de Postulación, cada vez que un trabajador se postula a un empleo.
Sólo se crea cuando éste se postula al empleo, cuya instancia ya se encuentra creada previamente. Por eso se 
postula. El trabajador cliquea, y se captura el id de la instancia Empleo. 
Se captura el id del usuario y se encuentra el trabajador en el backend y se lo asocia a la nueva instancia
Postulación que se crea.  
"""

class Postulacion(models.Model):
    empleo = models.ForeignKey(Empleo, on_delete=models.CASCADE)    
    trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE, blank=True, null=True)
    mensaje = models.CharField(max_length=100, blank=True, null=True)
    contratado = models.BooleanField(default=False)

    def set_estado_contratacion(self):
        self.contratado = True
        self.save()  


class Notification(models.Model):
    # nombre = models.CharField(max_length=100)
    user =  models.ForeignKey(User, on_delete=models.CASCADE)
    vista = models.BooleanField(default=False, blank=True, null=True)
    empleo = models.ForeignKey(Empleo, on_delete=models.CASCADE)
    estado = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return (f"la notificacion es del user: {self.user}")

