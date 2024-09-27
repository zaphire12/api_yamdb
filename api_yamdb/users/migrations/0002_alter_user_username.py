# Generated by Django 3.2 on 2024-09-27 12:15

from django.db import migrations, models

import users.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(error_messages={'unique': 'Пользователь с данным username уже существует.'}, max_length=150, unique=True, validators=[users.validators.validate_username], verbose_name='Имя пользователя'),
        ),
    ]
