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
from backend_api.serializers import UserSerializer, RegisterSerializer
from rest_framework.permissions import AllowAny

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
                print(f"retorna el token {token}")
                return Response({"token":token.key, "estado":create})
            else:
                return Response({'error': 'Wrong Credentials'}, status=401)
        
        else:
            return Response({'error': 'Faltan Credenciales'}, status=401)
        
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
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        print(f"esto llega {request}")
        content = {'message': 'Hello, from HelloView!'}
        return Response(content)

class HiView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        print(f"esto llega {request}")
        content = {'message': 'Hello, from HiView!'}
        return Response(content)


def get_api(request):
    url_token = "http://127.0.0.1:8000/api-token-auth/"
    body = {"username":"FrancoAlberti", "password":"40251206lampara0A"}
    r_token = requests.post(url_token, data=body).json().get("token")
    url = 'http://127.0.0.1:8000/hi/'
    headers = {'Authorization': f'Token {r_token}'}
    r = requests.get(url, headers=headers)
    return HttpResponse(r_token)