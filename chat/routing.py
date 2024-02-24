from django.urls import re_path, path
from . import consumers

websocket_urlpatterns = [
    # re_path(r"ws/chat/usuario/", consumers.ChatConsumer.as_asgi()),
    path('ws/notificaciones/', consumers.NotificacionesConsumer.as_asgi()),
    path('ws/alernotif/', consumers.AlertNotification.as_asgi()),
]
