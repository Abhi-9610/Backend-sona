# Generated by Django 5.0 on 2023-12-25 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loops', '0004_alter_loops_timestring'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loops',
            name='time_delay_seconds',
            field=models.IntegerField(null=True),
        ),
    ]
