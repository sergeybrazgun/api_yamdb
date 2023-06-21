# Generated by Django 3.2 on 2023-06-15 21:07

import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_auto_20230615_1251'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ('id',), 'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
        migrations.RemoveField(
            model_name='user',
            name='user_role',
        ),
        migrations.AddField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(default='XXXX', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(blank=True, choices=[('user', 'Пользователь'), ('admin', 'Админ'), ('moderator', 'Модератор')], default='user', max_length=20),
        ),
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=150, unique=True, validators=[django.core.validators.RegexValidator(re.compile('^[-a-zA-Z0-9_]+\\Z'), 'Enter a valid “slug” consisting of letters, numbers, underscores or hyphens.', 'invalid')]),
        ),
    ]
