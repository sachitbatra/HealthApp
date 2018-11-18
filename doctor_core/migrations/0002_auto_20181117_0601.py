# Generated by Django 2.0.4 on 2018-11-17 06:01

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor_core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consultation',
            name='no_days',
            field=models.IntegerField(default=3, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(0)]),
        ),
    ]
