# Generated by Django 5.0.1 on 2024-01-22 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rounds', '0003_score_yardage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='round',
            name='weather_conditions',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
