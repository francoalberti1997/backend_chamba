# Generated by Django 5.0 on 2024-01-02 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend_api', '0007_oferente_alter_empleo_oferente'),
    ]

    operations = [
        migrations.AddField(
            model_name='empleo',
            name='imagen_trabajo',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
