# Generated by Django 5.0 on 2024-01-29 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend_api', '0018_postulacion_contratado_postulacion_mensaje'),
    ]

    operations = [
        migrations.AddField(
            model_name='empleo',
            name='vigente',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='job',
            field=models.ManyToManyField(blank=True, related_name='usuarios_trabajo', to='backend_api.job'),
        ),
    ]