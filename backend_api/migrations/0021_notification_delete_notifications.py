# Generated by Django 5.0 on 2024-02-20 20:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend_api', '0020_notifications'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vista', models.BooleanField(blank=True, default=False, null=True)),
                ('estado', models.BooleanField(blank=True, null=True)),
                ('empleo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend_api.empleo')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Notifications',
        ),
    ]
