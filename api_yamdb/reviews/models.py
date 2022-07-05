from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from titles.models import Title

from users.models import User


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
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор обзора',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )
    score = models.PositiveSmallIntegerField(
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
        return f'Обзор:{self.text[:15]} - автор {self.author.username}'


class Comment(models.Model):
    """Модель комментариев к обзорам."""
    author = models.ForeignKey(
        User,
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
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return (
            f'Комментарий {self.text[:15]}'
            f'К обзору {self.review.text[:15]}'
            f'Автор {self.author.username}'
        )
