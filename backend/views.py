from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated  # <-- Here
import requests
from django.http import HttpResponse
from rest_framework.authtoken.models import Token
from rest_framework.authentication import authenticate
from django.contrib.auth.models import AbstractUser
from backend_api import models
from backend_api import serializers
from rest_framework import status
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from backend_api.serializers import UserSerializer, RegisterSerializer, UsuarioSerializer, JobSerializer, EmpleosSerializer,OferentesSerializer,PostulacionesSerializers, TrabajadorSerializer
from rest_framework.permissions import AllowAny
from django.utils import timezone
from datetime import timedelta
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from django.core.mail import EmailMessage, get_connection
from django.conf import settings
from backend_api.models import Usuario
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.db.models.query_utils import DeferredAttribute

# class RegisterView(APIView):
#     serializer_class = serializers.UserSerializer
#     permission_classes = (IsAuthenticated)    

class LogoutView(APIView):
    def post(self, request):
        user_token = request.META.get('HTTP_AUTHORIZATION')
        
        if user_token:
            user_token = user_token.replace('Token ', '').replace('Bearer ', '')

        try:
            token = Token.objects.get(key=user_token)
            token.delete()
            return Response({"message": "Token Eliminado. Sesión finalizada."})
        
        except Token.DoesNotExist:
                return Response({"error": "El token proporcionado no es válido"}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        if (request.data.get('username') and request.data.get('password')):
            user = authenticate(username = request.data['username'], password = request.data['password'])
            if user:
                token, create = Token.objects.get_or_create(user=user)
                try:
                    user = User.objects.get(username=user)
                    usuario = models.Usuario.objects.get(user=user.id)
                    now = timezone.now()
                    usuario.last_login = now - timedelta(hours=3)

                    usuario.save()
                    bool_usuario = True

                except models.Usuario.DoesNotExist as e:
                    bool_usuario = False

                except Exception as e:
                    print(f"Ocurrió un error: {e}")


                return Response({"token":token.key, "estado":create, "usuario":bool_usuario})
            else:
                return Response({'error': 'Wrong Credentials'}, status=401)
        
        else:
            return Response({'error': 'Faltan Credenciales'}, status=401)

class getUserLogueado(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self,request,*args,**kwargs):
        user = User.objects.get(id=request.user.id)
        
        try:
            usuario = models.Usuario.objects.get(user=user.id)
            bool_usuario = True

        except models.Usuario.DoesNotExist as e:
            bool_usuario = False

        except Exception as e:
            print(f"Ocurrió un error: {e}")

        return Response({"usuario_creado":bool_usuario})
    

class UserDetailAPI(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request,*args,**kwargs):
        user = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

class RegisterView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():   
            serializer.save()
            return Response({"mensaje":"usuario creado con éxito"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# def get_api(request):
#     url_token = "http://127.0.0.1:8000/api-token-auth/"
#     body = {"username":"FrancoAlberti", "password":"40251206lampara0A"}
#     r_token = requests.post(url_token, data=body).json().get("token")
#     url = 'http://127.0.0.1:8000/hi/'
#     headers = {'Authorization': f'Token {r_token}'}
#     r = requests.get(url, headers=headers)
#     return HttpResponse(r_token)


class UsuarioView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UsuarioSerializer

    def get(self,request,*args,**kwargs):
        usuario = models.Usuario.objects.all()
        serializer = UsuarioSerializer(usuario, many=True)
        return Response(serializer.data)    
    
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class UsuarioViewDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            usuario = Usuario.objects.get(user=request.user)
            serializer = UsuarioSerializer(usuario)
            return Response(serializer.data)
        except Usuario.DoesNotExist:
            return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
class JobView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = JobSerializer

    def get(self,request,*args,**kwargs):
        job = models.Job.objects.all()
        serializer = JobSerializer(job, many=True)
        return Response(serializer.data)    
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)



class ChangePassword(APIView):
    def _generate_and_send_token(self, user):
        usuario = Usuario.objects.get(email=user.email)
        token = usuario._generate_and_send_token()
        return token

    def post(self, request, *args, **kwargs):
        if request.data.get('username') and request.data.get('email'):
            username = request.data.get('username')
            email = request.data.get('email')
            print(f'Username: {username}, Email: {email}')

            try:
                user = User.objects.get(username=username, email=email)
                token = self._generate_and_send_token(user)
                return Response({'response': 'Mensaje Enviado'}, status=200)
            
            except User.DoesNotExist:
                return Response({'error': 'Usuario no encontrado en User'}, status=401)                
        else:
            return Response({'error': 'Faltan credenciales' }, status=401)
        
    def get(self, request, token, *args, **kwargs):
        try:
            usuario = Usuario.objects.get(password_reset_token=token)
        except Usuario.DoesNotExist:
            return Response({'error': 'Token no válido'}, status=404)
        except Exception as e:
            print(f'Error al procesar el token: {e}')
            return Response({'error': 'Error al procesar el token'}, status=500)

        # Verificar la vigencia del token
        expiration_time = timezone.now() - timezone.timedelta(hours=24)

        if usuario.password_reset_token_created_at < expiration_time:
            # El token ha caducado
            return Response({'error': 'Token ha caducado'}, status=400) 

        # Si el token es válido y no ha caducado, puedes devolver una respuesta exitosa

        return redirect(f"http://localhost:3000/reset_password/{token}/")

class ResetPassword(APIView):
    def get(self, request, token, *args, **kwargs):
        if token == "token_eliminado":
            return Response({'error': 'Token no válido token_eliminado'}, status=404)
        else:
            try:
                usuario = Usuario.objects.get(password_reset_token=token)
            except Usuario.DoesNotExist:
                return Response({'error': 'Token no válido'}, status=404)
            except Exception as e:
                print(f'Error al procesar el token: {e}')
                return Response({'error': 'Error al procesar el token'}, status=500)
            
            expiration_time = timezone.now() - timezone.timedelta(hours=24)

            if usuario.password_reset_token_created_at < expiration_time:
                # El token ha caducado
                return Response({'error': 'Token ha caducado'}, status=400)


            return Response({'Respuesta': f'{usuario}'}, status=200)

class Define_new_password(APIView):
    def post(self, request, token, *args, **kwargs):
        if token == "token_eliminado":
            return Response({'error': 'Token no válido token_eliminado'}, status=404)
        else:
            try:
                usuario = Usuario.objects.get(password_reset_token=token)
            except Usuario.DoesNotExist:
                return Response({'error': 'Token no válido'}, status=404)
            except Exception as e:
                print(f'Error al procesar el token: {e}')
                return Response({'error': 'Error al procesar el token'}, status=500)
            
            expiration_time = timezone.now() - timezone.timedelta(hours=24)
            if usuario.password_reset_token_created_at < expiration_time:
                # El token ha caducado
                return Response({'error': 'Token ha caducado'}, status=400)
            
        password = request.data.get('password')
        password2 = request.data.get('password2')
        username = request.data.get('username')

        if not (password and password2 and username):
            return Response({'error': 'Faltan credenciales'}, status=400)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=404)

        if password == password2:
            user.set_password(password)
            user.save()
            
            usuario = Usuario.objects.get(user=user)

            usuario._reset_token_null()
            usuario.show_token_password()
            return Response({'response': 'Contraseña cambiada exitosamente'}, status=201)
        else:
            return Response({'error': 'Las contraseñas no coinciden'}, status=400)

class Empleos_detail(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request, empleo=None, *args, **kwargs):

        empleos = models.Empleo.objects.get(id=empleo)
        serializers = EmpleosSerializer(empleos)
        return Response(serializers.data, status=200)

class Empleos(APIView):
    permission_classes = (IsAuthenticated,)    

    def get(self, request, user=None, *args, **kwargs):
        #Tiene que pasarle el id del usuario.
        if user:
            try:
                oferente = models.Oferente.objects.get(usuario__id=user)
            except models.Oferente.DoesNotExist:
                return Response({'error': 'Oferente no encontrado'}, status=404)

            jobs = models.Empleo.objects.filter(oferente=oferente)
        else:
            try:
                usuario = Usuario.objects.get(user=request.user.id)

                try:
                    trabajador = usuario.trabajador #295
                    
                    postulaciones = models.Postulacion.objects.filter(trabajador=trabajador)
                    empleos_postulados = [postulacion.empleo for postulacion in postulaciones]
                        
                    jobs = models.Empleo.objects.exclude(pk__in=[empleo.pk for empleo in empleos_postulados])

                except models.Trabajador.DoesNotExist:
                    jobs = models.Empleo.objects.all()

            except Usuario.DoesNotExist:
                return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
            except models.Trabajador.DoesNotExist:
                return Response({"error": "Trabajador no encontrado. Arreglar linea 295"}, status=status.HTTP_404_NOT_FOUND)
            except models.Postulacion.DoesNotExist:
                return Response({"error": "No hay postulaciones"}, status=status.HTTP_404_NOT_FOUND)



        serializer = EmpleosSerializer(jobs, many=True)

        for empleo_data in serializer.data:
            oferente_id = empleo_data.get('oferente')
            if oferente_id:
                oferente = models.Oferente.objects.get(id=oferente_id)
                usuario = oferente.usuario
                empleo_data['usuario'] = {
                    'nombre': usuario.nombre,
                    'apellido': usuario.apellido,
                    'imagen': str(usuario.foto_perfil),
                }

        return Response(serializer.data, status=200)

    def post(self, request, *args, **kwargs):
        try:
            usuario = Usuario.objects.get(user=request.user)
            oferente_instance = models.Oferente.objects.filter(usuario=usuario).first()
        except Usuario.DoesNotExist:
            return Response({'errors': "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        

        if not oferente_instance:
            # Si no existe, crea un nuevo Oferente
            oferente_instance = models.Oferente(usuario=usuario)
            oferente_instance.save()

        # Crear un diccionario mutable a partir de QueryDict
        mutable_data = request.data.copy()

        # Añadir el ID del oferente al diccionario
        mutable_data["oferente"] = oferente_instance.id

        serializer = EmpleosSerializer(data=mutable_data)

        if serializer.is_valid():
            # Accede al objeto Empleo antes de guardarlo
            empleo = serializer.save()

            # Asigna el Oferente al Empleo
            empleo.oferente = oferente_instance

            # Guarda finalmente el objeto Empleo con el Oferente asociado
            empleo.vigente = True

            empleo.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Devuelve los errores de validación en la respuesta
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



class ShowOferente(APIView):
    def get(self, request, *args, **kwargs):
        oferente = models.Oferente.objects.all()
        serializer = OferentesSerializer(oferente, many=True)
        return Response(serializer.data, status=200)
        
class ShowOferente_user(APIView):
    permission_classes = (IsAuthenticated,)    

    def get(self, request, *args, **kwargs):
        try:
            usuario = Usuario.objects.get(user=request.user)
            # oferente = models.Oferente.objects.filter(usuario=usuario).first()
            return Response({"id_oferente":usuario.id}, status=200)
        except:
            return Response({"error":"No encontradp"}, status=401)


class PostulacionList(APIView):
    permission_classes = (IsAuthenticated,)    

    def get(self, request, *args, **kwargs):
        try:
            usuario = Usuario.objects.get(user=request.user.id)
            print(usuario)
            trabajador = usuario.trabajador  # Asumiendo que la relación es directa
            # trabajador = models.Trabajador.objects.get(usuario=usuario)  # Alternativa si la relación es indirecta

            print("Trabajador encontrado:")
            print(trabajador)

            postulaciones = models.Postulacion.objects.filter(trabajador=trabajador)


            trabajadores_data = []

            for postulacion in postulaciones:
                foto_perfil_url = postulacion.empleo.imagen_trabajo.url if postulacion.empleo.imagen_trabajo else None
                
                # Convertir a lista las habilidades

                trabajador_data = {
                    "empleo":{
                        "oferente":postulacion.empleo.oferente.usuario.nombre + " " + postulacion.empleo.oferente.usuario.apellido,
                        "titulo":postulacion.empleo.titulo,
                        "barrio":postulacion.empleo.barrio,
                        "ciudad":postulacion.empleo.ciudad,
                        "provincia":postulacion.empleo.provincia,
                        "fecha_creacion":postulacion.empleo.fecha_creacion,
                        "trabajo":postulacion.empleo.trabajo,
                        "oferta":postulacion.empleo.oferta,
                        "descripcion":postulacion.empleo.descripcion,
                        "vigente":postulacion.empleo.vigente,
                        "imagen_trabajo":foto_perfil_url,
                    },
                    "mensaje":postulacion.mensaje,
                    "contratado":postulacion.contratado,
                }

                trabajadores_data.append(trabajador_data)

            return Response({"mensaje":trabajadores_data}, status=200)
        
        except Usuario.DoesNotExist:
            return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except models.Trabajador.DoesNotExist:
            return Response({"error": "Trabajador no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except models.Postulacion.DoesNotExist:
            return Response({"error": "No hay postulaciones"}, status=status.HTTP_404_NOT_FOUND)


    def post(self, request, *args, **kwargs):
        print(request.data)

        usuario_id = request.data.get("usuario")
        empleo_id = request.data.get("empleo")

        # Si hay un mensaje incluido
        mensaje = request.data.get("mensaje", "")
        
        # usuario = get_object_or_404(User, id=usuario_id)

        # print(f"el usuario es {usuario}")

        try:
            usuario_id = int(usuario_id)
            print("usuario id ok")
        except ValueError:
            return Response({'errors': "Usuario ID no válido"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            trabajador = models.Trabajador.objects.get(usuario_id=usuario_id)
        except models.Trabajador.DoesNotExist:
            trabajador = models.Trabajador.objects.create(usuario_id=usuario_id)
            print("se acaba de crear uno")

        try:
            empleo = models.Empleo.objects.get(id=empleo_id)
        except models.Empleo.DoesNotExist:
            return Response({'errors': "Empleo no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        data = {"empleo": empleo.id, "trabajador": trabajador.id, "mensaje": mensaje}
        
        postulacion = models.Postulacion.objects.filter(empleo=empleo.id, trabajador=trabajador.id)

        if len(postulacion) >= 1:
            return Response({'error': "Ya se postuló"}, status=status.HTTP_400_BAD_REQUEST)

    
        serializer = serializers.PostulacionesSerializers(data=data)

        if serializer.is_valid():
            propuesta = serializer.save()
            propuesta.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            # Devuelve los errores de validación en la respuesta
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class PostulacionDetail(APIView):
    #problema. No verifica que la el oferente en empleo en postulación, sea el usuario que la solicita.
    # agregar que request.user sea usuario en oferente en empleo en postulacion
    permission_classes = (IsAuthenticated,)    

    def get(self, request, empleo=None, *args, **kwargs):
        if empleo:
            empleo_instance = models.Empleo.objects.filter(id=empleo).first()
            if empleo_instance:

                oferente = empleo_instance.return_oferente()
                usuario = str(oferente.usuario)
                usuario_dueño = str(request.user)
                

                if (usuario == usuario_dueño):
          
                    postulaciones = models.Postulacion.objects.filter(empleo=empleo_instance)
                    postulaciones_data = []

                    for postulacion in postulaciones:
                        usuario = postulacion.trabajador.usuario
                        foto_perfil_url = usuario.foto_perfil.url if usuario.foto_perfil else None

                        postulacion_data = {
                            "id": postulacion.id,
                            "empleo": postulacion.empleo.id,
                            "experiencia":postulacion.trabajador.experiencia,
                            "calificaciones":postulacion.trabajador.calificaciones,
                            "trabajador": {
                                "id": usuario.id,
                                "nombre": usuario.nombre,
                                "apellido": usuario.apellido,
                                "foto_perfil": foto_perfil_url,
                                "ciudad": usuario.ciudad
                            },
                            "mensaje": postulacion.mensaje,
                            "contratado": postulacion.contratado,
                        }

                        postulaciones_data.append(postulacion_data)
                    
                    return Response({"mensaje": postulaciones_data}, status=200)
                else:
                    print(f"usuario: {usuario}, usuario_dueño:{usuario_dueño}")
                    return Response({'error': 'No eres el dueñssso de este empleo'}, status=404)
            else:
                return Response({'error': 'Empleo no encontrado'}, status=404)
        else:
            return Response({'error': 'Empleo no provisto'}, status=404)
    

    def post(self, request, empleo=None, *args, **kwargs):

        usuario_id = request.data.get("usuario") #Usuario del trabajador seleccionado
        
        if empleo:
            try:
                trabajador = models.Trabajador.objects.get(usuario_id=usuario_id)
                empleo_instance = models.Empleo.objects.get(id=empleo)

            except models.Trabajador.DoesNotExist:
                return Response({"error": "no hay trabajador con ese ID"}, status=status.HTTP_400_BAD_REQUEST)

            except models.Empleo.DoesNotExist:
                return Response({"error": "no hay Empleo con ese ID"}, status=status.HTTP_400_BAD_REQUEST)

            if (request.user == empleo_instance.oferente.usuario.user):

                postulacion = models.Postulacion.objects.filter(empleo=empleo_instance.id, trabajador=trabajador.id).first()
                
                if postulacion:
                    postulacion.set_estado_contratacion()
                    postulacion.empleo.set_vigente()

                    return Response({"mensaje":"modificado"}, status=status.HTTP_200_OK)
              
                else:
                    return Response({'error': 'No se encontró la Postulacion'}, status=status.HTTP_404_NOT_FOUND)

            else:
                return Response({'error': 'Id No corresponde al oferente'}, status=status.HTTP_404_NOT_FOUND)


        return Response({'error': 'Empleo no provisto'}, status=status.HTTP_404_NOT_FOUND)




class TrabajadoresList(APIView):
    permission_classes = (IsAuthenticated,)    

    def get(self, request, *args, **kwargs):
        trabajadores = models.Trabajador.objects.all()

        trabajadores_data = []

        for trabajador in trabajadores:
            usuario = trabajador.usuario
            foto_perfil_url = usuario.foto_perfil.url if usuario.foto_perfil else None
            
            habilidades = [job.job for job in trabajador.habilidades.all()]  # Convertir a lista las habilidades
             # Convertir a lista las habilidades
            trabajador_data = {
                "id":trabajador.id,
                "usuario":{
                    "nombre":usuario.nombre,
                    "apellido":usuario.apellido,
                    "foto_perfil":foto_perfil_url,
                    "ciudad":usuario.ciudad,
                    "provincia":usuario.provincia,
                    "edad":usuario.edad,
                    "sexo":usuario.sexo,
                },
                "habilidades": habilidades,  # Usar la lista de habilidades, que es la lista jobs de usuario, o debería serlo
                "experiencia": trabajador.experiencia,
                "calificaciones": trabajador.calificaciones,
            }

            trabajadores_data.append(trabajador_data)

        return Response({"mensaje": trabajadores_data}, status=200)


class NotificacionesVista(APIView):
    permission_classes = (IsAuthenticated,)    

    def post(self, request, *args, **kwargs):
        
        id_notificacion = request.data.get("notificacion").get("id_notificacion")

        notificacion = models.Notification.objects.filter(id=id_notificacion).first()
        notificacion.vista = True
        notificacion.save()

        return Response({"mensaje": "usuario"}, status=200)

    def get(self, request, *args, **kwargs):
        usuario_id = request.user.id
        notificaciones = models.Notification.objects.filter(user=usuario_id)
        contador = 0
        for i in notificaciones:
            if (not(i.vista)): #si es falsa, o sea, si no se vió la notificación
                contador += 1
            else:
                pass

        return Response({"contador":contador})