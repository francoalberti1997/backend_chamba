from urllib.parse import parse_qs
from django.contrib.auth.models import User
from backend_api.models import Notification, Empleo
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import async_to_sync
from backend_api.models import Usuario

class NotificacionesConsumer(AsyncWebsocketConsumer):
   
    @database_sync_to_async
    def get_user_by_token(self, token):
        try:
            user = User.objects.get(auth_token=token)
            return user
        except User.DoesNotExist:
            return None
    
    @database_sync_to_async
    def get_usuario_by_username(self, username):
        try:
            user = User.objects.get(username=username)
            return user
        except User.DoesNotExist:
            return None
    
    @database_sync_to_async
    def get_notif_by_usuario(self, user_id):
        try:
            notif = Notification.objects.select_related().filter(user=user_id)
            
            notif_lista = []

            for i in notif:

                obj = {
                    "user":i.user.username,
                    "vista":i.vista,
                    "empleo":i.empleo.titulo,
                    "estado":i.estado,
                    "fecha":i.empleo.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S'),
                    "imagen":i.empleo.imagen_trabajo.url,
                    "id_notificacion":i.id
                }
                notif_lista.append(obj)

            return notif_lista
        #devolve un objeto construido con lo que vos querés
        except Notification.DoesNotExist:
            return None


        
    async def connect(self):
        self.group_name = "notification"    
        await self.accept()

        query_string = self.scope['query_string'].decode()
        params = parse_qs(query_string)
        token = params.get('token', [''])[0]

        self.user = await self.get_user_by_token(token)

        if self.user:
            usuario = await self.get_usuario_by_username(self.user.username)

            if usuario:
                notif = await self.get_notif_by_usuario(usuario)
                

            #     notification_data = {
            #     "user": [i.user.username for i in notif],  # Si deseas enviar solo el nombre de usuario
            #     "empleo": [i.empleo.id for i in notif],  # O cualquier otro campo serializable, como el ID
            #     "estado": [i.estado for i in notif]
            # }

            await self.send(text_data=json.dumps(notif))


class AlertNotification(AsyncWebsocketConsumer):
    @database_sync_to_async
    def get_user_by_token(self, token):
        try:
            user = User.objects.get(auth_token=token)
            return user
        except User.DoesNotExist:
            return None
    
    @database_sync_to_async
    def get_usuario_by_id_user(self, user_id):
        try:
            usuario = Usuario.objects.get(id=user_id) #Tiene que recibir el id del usuario
            return usuario.user
        
        except Usuario.DoesNotExist:
            return None
    
    @database_sync_to_async
    def createNotification(self, user_id, empleo_id, estado):
        notificacion = Notification.objects.create(user=user_id, estado=estado, empleo=empleo_id) 
        return notificacion
    
    @database_sync_to_async
    def getEmpleo(self, empleo_id):
        notificacion = Empleo.objects.filter(id=empleo_id).first()
        return notificacion
    
    @database_sync_to_async
    def get_number_of_Notif_by_user(self, user_id):
        notificacion = Notification.objects.select_related().filter(user=user_id)
        contador = 0

        for i in notificacion:
            if (not(i.vista)): #si es falsa, o sea, si no se vió la notificación
                contador += 1
            else:
                pass

        return contador



    async def connect(self):
        self.room_group_name = "AlertNotif"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        query_string = self.scope['query_string'].decode()
        params = parse_qs(query_string)
        token = params.get('token', [''])[0]

        self.user = await self.get_user_by_token(token)

        number_notifs = await self.get_number_of_Notif_by_user(self.user.id)

        await self.accept()

        await self.send(text_data=json.dumps(number_notifs))



    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": message}
        )

    # Receive message from room group
    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        trabajador_id = message['id_trabajador']
        token_empleador = message["token"]
        empleo_id = message["empleo"]

        
        trabajador = await self.get_usuario_by_id_user(trabajador_id)
        empleador = await self.get_user_by_token(token_empleador)

        query_string = self.scope['query_string'].decode()
        params = parse_qs(query_string)
        token = params.get('token', [''])[0]

        self.user = await self.get_user_by_token(token)

        empleo = await self.getEmpleo(empleo_id)

        print("NOTIFICACION")
        print(f"self.user: {self.user}, trabajador: {trabajador}")

        if (self.user == trabajador):
            #manejar caso en que el trabajador es el seleccionado.
            #crear notificacion 
            # print("va a crearse la notificacion")
            await self.createNotification(self.user, empleo, estado=True)

            number_notifs = await self.get_number_of_Notif_by_user(self.user.id)
          
            if self.user is not None:
                # print("va a enviarse True")
                #enviar el contador de notifs no vistas
                await self.send(text_data=json.dumps(number_notifs))
            else:
                # print("NO va a enviarse True")
                await self.send(text_data=json.dumps(False))
        else:
            pass