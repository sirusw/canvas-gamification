# Generated by Django 3.0.14 on 2022-01-13 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0024_auto_20211203_1955'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='time_spent',
            field=models.IntegerField(default=0),
        ),
    ]
