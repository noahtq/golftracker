# Generated by Django 5.0.1 on 2024-01-21 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courselibrary', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tee',
            name='course_rating',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tee',
            name='slope_rating',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
