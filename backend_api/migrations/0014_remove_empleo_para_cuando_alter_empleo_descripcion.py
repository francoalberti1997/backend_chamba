# Generated by Django 5.0 on 2024-01-03 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend_api', '0013_empleo_para_cuando'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='empleo',
            name='para_cuando',
        ),
        migrations.AlterField(
            model_name='empleo',
            name='descripcion',
            field=models.CharField(max_length=500),
        ),
    ]
