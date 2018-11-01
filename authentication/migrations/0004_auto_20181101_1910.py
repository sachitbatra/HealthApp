# Generated by Django 2.1.2 on 2018-11-01 13:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_sessiontoken'),
    ]

    operations = [
        migrations.CreateModel(
            name='DoctorModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email_address', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=4096)),
            ],
        ),
        migrations.RemoveField(
            model_name='usermodel',
            name='age',
        ),
        migrations.AddField(
            model_name='usermodel',
            name='dateOfBirth',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
