# Generated by Django 3.0.14 on 2022-01-24 07:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0025_submission_time_spent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submission',
            name='time_spent',
        ),
    ]
