# Generated by Django 5.0 on 2024-01-02 07:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend_api', '0006_empleo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Oferente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prob_jugo', models.FloatField(blank=True, null=True)),
                ('nro_transacciones', models.IntegerField(default=0)),
                ('nro_transacciones_ofertadas', models.IntegerField(default=0)),
                ('seriedad', models.FloatField(blank=True, null=True)),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='backend_api.usuario')),
            ],
        ),
        migrations.AlterField(
            model_name='empleo',
            name='oferente',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='backend_api.oferente'),
        ),
    ]
