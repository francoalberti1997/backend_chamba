# Generated by Django 5.0 on 2024-01-08 20:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend_api', '0015_alter_empleo_fecha_creacion_alter_empleo_trabajo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postulacion',
            name='trabajador',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='backend_api.trabajador'),
        ),
    ]
