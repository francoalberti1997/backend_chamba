# Generated by Django 5.0 on 2023-12-31 04:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend_api', '0005_usuario_password_reset_token_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Empleo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(blank=True, max_length=50, null=True)),
                ('barrio', models.CharField(blank=True, max_length=50, null=True)),
                ('ciudad', models.CharField(blank=True, max_length=50, null=True)),
                ('provincia', models.CharField(blank=True, max_length=50, null=True)),
                ('fecha_creacion', models.DateTimeField(blank=True, null=True)),
                ('trabajo', models.CharField(blank=True, choices=[('limpieza', 'por hora de trabajo'), ('reparacion', 'por trabajo completo')], max_length=100, null=True)),
                ('oferta', models.IntegerField(blank=True, null=True)),
                ('descripcion', models.CharField(max_length=200)),
                ('oferente', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='backend_api.usuario')),
            ],
        ),
    ]