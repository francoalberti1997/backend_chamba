from django.contrib import admin
from . import models

admin.site.register(models.Usuario)
admin.site.register(models.Job) 
admin.site.register(models.Empleo) 
admin.site.register(models.Oferente) 
admin.site.register(models.Postulacion) 
admin.site.register(models.Trabajador) 
admin.site.register(models.Notification) 