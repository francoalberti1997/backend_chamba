"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token  # <-- Here
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('get_api/', views.get_api, name='get_api'),
    path('login-view/', views.LoginView.as_view(), name='login-view'),
    path('logout-view/', views.LogoutView.as_view(), name='logout-view'),
    path('register', views.RegisterView.as_view(), name="register"),
    path('get_user', views.UserDetailAPI.as_view(), name="get_user"),
    path('usuario/', views.UsuarioView.as_view(), name="usuario_view"),
    path('job/', views.JobView.as_view(), name="job_view"),
    #Reestablecer Contraseña
    path('change_password/', views.ChangePassword.as_view(), name="change_password"),
    path('reset_password/<token>/', views.ChangePassword.as_view(), name="change_password_token"),
    path('reset_password_user/<token>/', views.ResetPassword.as_view(), name="reset_password_token"),
    path('define_new_password/<token>/', views.Define_new_password.as_view(), name="define_new_passwords"),
    path('empleos/', views.Empleos.as_view(), name="Empleos-list"),
    path('empleos/<int:user>/', views.Empleos.as_view(), name="Empleos-list-with-user"), #PASANDO EL USER, DEVUELVE LOS EMPLEOS (LISTA) OFERTADOS POR ESE OFERENTE
    path('empleos_detail/<int:empleo>/', views.Empleos_detail.as_view(), name="Empleo-list"),
    path('oferentes/', views.ShowOferente.as_view(),    name="oferentes"),
    path('oferentes/user/', views.ShowOferente_user.as_view(), name="oferentes_user"),
    path('usuario_detail/', views.UsuarioViewDetail.as_view(), name="usuario_details"),
    path('postulaciones/', views.PostulacionList.as_view(), name="postulaciones_list"),
    path('postulaciones_detail/<int:empleo>/', views.PostulacionDetail.as_view(), name="postulaciones_list"),
    path('trabajadores/', views.TrabajadoresList.as_view(), name="trabajadores_list"),
    path('getUserLogueado/', views.getUserLogueado.as_view(), name="getUserLogueado"),
    path('vistaNotificacion/', views.NotificacionesVista.as_view(), name="NotificacionesVista"),

    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
