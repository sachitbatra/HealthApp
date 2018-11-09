# Generated by Django 2.1.2 on 2018-11-09 20:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('first', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_thread_first', to='authentication.AppUser')),
                ('second', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_thread_second', to='authentication.AppUser')),
            ],
        ),
        migrations.AddField(
            model_name='chatmessage',
            name='thread',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='consultation.Thread'),
        ),
        migrations.AddField(
            model_name='chatmessage',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.AppUser', verbose_name='sender'),
        ),
    ]
