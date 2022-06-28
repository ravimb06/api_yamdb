from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from titles.models import Title
from api.validators import validate_year
from users.models import #  Наш переопределенный юзер


class Review(models.Model):
    """Модель Обзоров на произведения."""
    title = models.ForeignKey(
        Title, 
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Название произведения',
    )
    text = models.TextField(verbose_name='Текст обзора')
    author = models.ForeignKey(
        #  Наш переопределенный юзер,
        on_delete=models.CASCADE,
        verbose_name='Автор обзора',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )
    score = models.IntegerField(
        verbose_name='Оценка',
        validators=(
            MinValueValidator(
                1,
                message='Число должно быть от 1 до 10'
            ),
            MaxValueValidator(
                10,
                message='Число должно быть от 1 до 10'
            )
        )
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Обзор'
        verbose_name_plural = 'Обзоры'
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='review_on_title'
            ),
        ]

    def __str__(self):
        return f'Обзор:{self.text[:15]} - автор {self.author}'


class Comment(models.Model):
    """Модель комментариев к обзорам."""
    author = models.ForeignKey(
        #  Наш переопределенный юзер,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария',
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Обзор',
    )
    text = models.TextField(verbose_name='Текст комментария')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата коментария',
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Комментарий'
    
    def __str__(self):
        return (
            f'Комментарий {self.text[:15]}'
            f'К обзору {self.review[:15]}'
            f'Автор {self.author}'
        )


class Category(models.Model):
    name = models.CharField('название', max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ('name', )
        verbose_name = 'категория'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField('название', max_length=256)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('name', )
        verbose_name = 'жанр'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField('название', max_length=256)
    year = models.SmallIntegerField('год', validators=(validate_year,))
    description = models.TextField(
        'описание',
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='жанр'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='категория',
        null=True,
        blank=True
    )

    class Meta:
        ordering = ('name', )
        verbose_name = 'произведение'

    def __str__(self):
        return self.name
