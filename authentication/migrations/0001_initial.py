# Generated by Django 2.1.2 on 2018-11-21 06:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AppUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email_address', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=4096)),
                ('dateOfBirth', models.DateTimeField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='DoctorSessionToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_token', models.CharField(max_length=255)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserSessionToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_token', models.CharField(max_length=255)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='DoctorModel',
            fields=[
                ('appuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='authentication.AppUser')),
                ('specialization', models.CharField(max_length=255)),
                ('auth_document', models.FileField(upload_to='authenticationDocs')),
                ('auth_document_url', models.CharField(max_length=255)),
                ('degree', models.CharField(max_length=255)),
                ('experience', models.IntegerField()),
                ('verified', models.BooleanField(default=False)),
            ],
            bases=('authentication.appuser',),
        ),
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('appuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='authentication.AppUser')),
            ],
            bases=('authentication.appuser',),
        ),
        migrations.AddField(
            model_name='usersessiontoken',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.UserModel'),
        ),
        migrations.AddField(
            model_name='doctorsessiontoken',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.DoctorModel'),
        ),
    ]
