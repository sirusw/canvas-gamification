# Generated by Django 3.0.3 on 2020-03-15 00:05

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0013_javasubmission'),
    ]

    operations = [
        migrations.AddField(
            model_name='javasubmission',
            name='results',
            field=jsonfield.fields.JSONField(default=dict),
        ),
    ]