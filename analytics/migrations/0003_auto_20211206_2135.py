# Generated by Django 3.0.14 on 2021-12-07 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0002_auto_20211206_2134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionanalytics',
            name='event',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='questionanalytics',
            name='question',
            field=models.IntegerField(default=0),
        ),
    ]
