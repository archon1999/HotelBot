# Generated by Django 3.2 on 2022-03-21 13:52

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BotUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_id', models.CharField(max_length=255, unique=True)),
                ('first_name', models.CharField(max_length=255, verbose_name='Имя')),
                ('last_name', models.CharField(blank=True, max_length=255, null=True)),
                ('username', models.CharField(blank=True, max_length=255, null=True)),
                ('bot_state', models.IntegerField(default=0)),
                ('lang', models.CharField(default='uz', max_length=2)),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(choices=[(1, 'Message'), (2, 'Key'), (3, 'Smile')])),
                ('title', models.CharField(max_length=255)),
                ('body_uz', models.TextField()),
                ('body_ru', models.TextField()),
                ('body_en', models.TextField()),
            ],
            managers=[
                ('templates', django.db.models.manager.Manager()),
            ],
        ),
    ]
