# Generated by Django 5.0 on 2023-12-26 06:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend_api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='usuarios',
        ),
    ]
