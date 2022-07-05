from django.core.validators import MaxValueValidator
from django.db import models
from django.utils import timezone


class Category(models.Model):
    """Модель категории произведения."""
    name = models.CharField(
        max_length=50,
        verbose_name='Название категории',
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Короткое название',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'Категория - {self.name}'


class Genre(models.Model):
    """Модель жанра произведения."""
    name = models.CharField(
        max_length=60,
        verbose_name='Название жанра',
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Короткое название',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return f'Жанр - {self.name}'


class Title(models.Model):
    """Модель произведения."""
    name = models.CharField(
        max_length=100,
        verbose_name='Название произведения',
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание',
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        related_name='titles',
        verbose_name='Жанр',
    )
    year = models.PositiveSmallIntegerField(
        validators=(
            MaxValueValidator(
                int(timezone.now().year),
                message='Нельзя указывать год, больше текущего',
            ),

        ),
        verbose_name='Год',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='titles',
        verbose_name='Категория',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return (
            f'Произведение {self.name} - Категория {self.category}'
            f'Жанр {self.genre} - Год релиза {self.year}'
        )
