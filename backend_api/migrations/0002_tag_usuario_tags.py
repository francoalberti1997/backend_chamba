# Generated by Django 4.2.5 on 2023-12-23 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend_api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='usuario',
            name='tags',
            field=models.ManyToManyField(related_name='posts', to='backend_api.tag'),
        ),
    ]
