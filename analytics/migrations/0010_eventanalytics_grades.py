# Generated by Django 3.0.14 on 2022-01-31 04:49

import course.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0009_auto_20220129_1219'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventanalytics',
            name='grades',
            field=course.fields.JSONField(default=dict),
        ),
    ]
