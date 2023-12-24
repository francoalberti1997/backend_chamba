from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

class Tag(models.Model):
    name = models.CharField(max_length=255)

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    foto_perfil = models.ImageField()
    ciudad = models.CharField(max_length=65)
    provincia = models.CharField(max_length=65)
    edad = models.IntegerField()

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

    profesion = models.CharField(max_length=100, choices=profesion_CHOICES)


    sexo_CHOICES = [
            ('H', 'Hombre'),
            ('M', 'Mujer'),
        ]

    sexo = models.CharField(max_length=20, choices=sexo_CHOICES)
    tags = models.ManyToManyField(to=Tag, related_name="posts")

    def __str__(self):
        return self.ciudad

