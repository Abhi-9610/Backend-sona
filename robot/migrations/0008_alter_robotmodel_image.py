# Generated by Django 5.0 on 2024-01-09 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('robot', '0007_alter_goalsmodel_audio_alter_robotmodel_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='robotmodel',
            name='image',
            field=models.ImageField(upload_to='public/uploads/images/profile/robot/'),
        ),
    ]
