# Generated by Django 3.0.14 on 2022-01-24 20:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('analytics', '0005_auto_20220124_1216'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='javaquestionanalytics',
            options={'base_manager_name': 'objects'},
        ),
        migrations.AlterModelOptions(
            name='mcqquestionanalytics',
            options={'base_manager_name': 'objects'},
        ),
        migrations.AlterModelOptions(
            name='parsonsquestionanalytics',
            options={'base_manager_name': 'objects'},
        ),
        migrations.AlterModelOptions(
            name='questionanalytics',
            options={'base_manager_name': 'objects'},
        ),
        migrations.AddField(
            model_name='questionanalytics',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_analytics.questionanalytics_set+', to='contenttypes.ContentType'),
        ),
    ]
