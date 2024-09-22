# Generated by Django 3.2 on 2024-09-22 00:27

from django.db import migrations, models
import django.db.models.deletion
import reviews.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categorie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите название категории', max_length=256, verbose_name='Название категории')),
                ('slug', models.SlugField(unique=True, verbose_name='Метка')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите название жанра', max_length=256, verbose_name='Название жанра')),
                ('slug', models.SlugField(unique=True, verbose_name='Метка')),
            ],
            options={
                'verbose_name': 'Жанр',
                'verbose_name_plural': 'Жанры',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Название произведения')),
                ('year', models.PositiveIntegerField(validators=[reviews.validators.validate_year_release], verbose_name='Год выпуска')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание произведения')),
                ('category', models.OneToOneField(help_text='Категория, к которому относится произведение', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='titles', to='reviews.categorie', verbose_name='Категория')),
                ('genre', models.ForeignKey(blank=True, help_text='Жанры, к которым относится произведение', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='categories', to='reviews.genre', verbose_name='Жанр')),
            ],
            options={
                'verbose_name': 'Произведение',
                'verbose_name_plural': 'Произведения',
                'ordering': ('name',),
            },
        ),
    ]
