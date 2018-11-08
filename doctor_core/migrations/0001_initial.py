# Generated by Django 2.1.2 on 2018-11-07 23:52

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Consultation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no_days', models.IntegerField(default=3, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(3)])),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('diagnosis', models.TextField(blank=True)),
                ('notes', models.TextField(blank=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.DoctorModel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.UserModel')),
            ],
        ),
        migrations.CreateModel(
            name='DoctorProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True)),
                ('image', models.ImageField(blank=True, height_field='height_field', null=True, upload_to='', width_field='width_field')),
                ('height_field', models.IntegerField(default=0)),
                ('width_field', models.IntegerField(default=0)),
                ('phone_no', models.CharField(blank=True, max_length=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='authentication.DoctorModel')),
            ],
        ),
        migrations.CreateModel(
            name='FeedBack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback', models.TextField(blank=True)),
                ('overall_rating', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(0)])),
                ('quickness', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(0)])),
                ('treatment', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(0)])),
                ('consultation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doctor_core.Consultation')),
            ],
        ),
    ]
