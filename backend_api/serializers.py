from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import Usuario, Job, Empleo, Oferente, Postulacion, Trabajador
from django.utils import timezone
from datetime import timedelta

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = "__all__"

class UsuarioSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Usuario
        fields = "__all__"

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
    required=True,
    validators=[UniqueValidator(queryset=User.objects.all())])
  
    password = serializers.CharField(
    write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2',
                'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
            {"password": "Password fields didn't match."})
        return attrs
        
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            #verificar que el email no exista
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )   
        user.set_password(validated_data['password'])
        
        user.save()
        return user


class OferentesSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer()

    class Meta:
        model = Oferente
        fields = ['usuario']

class EmpleosSerializer(serializers.ModelSerializer):

    class Meta:
        model = Empleo
        fields = "__all__"


class TrabajadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trabajador
        fields = ('id', 'usuario', 'habilidades', 'experiencia', 'calificaciones')

class PostulacionesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Postulacion
        fields = "__all__"
