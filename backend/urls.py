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
    path('hello/', views.HelloView.as_view(), name='hello'),
    path('hi/', views.HiView.as_view(), name='hi'),
    path('get_api/', views.get_api, name='get_api'),
    path('login-view/', views.LoginView.as_view(), name='login-view'),
    path('logout-view/', views.LogoutView.as_view(), name='logout-view'),
    path('register', views.RegisterView.as_view(), name="register"),
    path('get_user', views.UserDetailAPI.as_view(), name="get_user")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
