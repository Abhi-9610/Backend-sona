# Generated by Django 5.0 on 2024-01-08 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('robot', '0005_remove_goalsmodel_own'),
    ]

    operations = [
        migrations.AlterField(
            model_name='robotmodel',
            name='image',
            field=models.ImageField(upload_to='media/public/uploads/images/robot'),
        ),
    ]
