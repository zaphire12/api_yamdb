from django.db import models

from users.models import User
from reviews.validators import validate_year_release


class Categorie(models.Model):
    """Категории (типы) произведений."""

    name = models.CharField(
        max_length=256,
        verbose_name='Название категории',
        help_text='Введите название категории'
    )
    slug = models.SlugField(max_length=50, unique=True, verbose_name='Метка')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Категории жанров."""

    name = models.CharField(
        max_length=256,
        verbose_name='Название жанра',
        help_text='Введите название жанра'
    )
    slug = models.SlugField(max_length=50, unique=True, verbose_name='Метка')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Произведения (определённый фильм, книга или песенка)."""

    name = models.CharField(
        max_length=256,
        verbose_name='Название произведения',
    )
    year = models.PositiveIntegerField(
        verbose_name='Год выпуска', validators=[validate_year_release]
    )
    description = models.TextField(
        null=True, blank=True, verbose_name='Описание произведения'
    )
    category = models.OneToOneField(
        Categorie,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        verbose_name='Категория',
        help_text='Категория, к которому относится произведение'
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='categories',
        verbose_name='Жанр',
        help_text='Жанры, к которым относится произведение'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return f'{self.name}, {self.year}, {self.category}, {self.genre}'
