# Generated by Django 5.0 on 2024-01-09 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('robot', '0011_alter_goalsmodel_audio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='robotmodel',
            name='image',
            field=models.ImageField(upload_to='uploads/images/robots/'),
        ),
    ]
