# Generated by Django 5.0 on 2024-01-09 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('robot', '0006_alter_robotmodel_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goalsmodel',
            name='audio',
            field=models.FileField(upload_to='public/uploads/images/audioclip/'),
        ),
        migrations.AlterField(
            model_name='robotmodel',
            name='image',
            field=models.ImageField(upload_to='public/uploads/images/robot/'),
        ),
    ]
