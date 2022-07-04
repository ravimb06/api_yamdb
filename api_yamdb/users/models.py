from django.contrib.auth.models import AbstractUser
from django.db import models

from users.validators import UsernameValidator

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'


class User(AbstractUser):

    ROLES = (
        (USER, USER),
        (MODERATOR, MODERATOR),
        (ADMIN, ADMIN),
    )
    username_validator = UsernameValidator()
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        unique=True,
        validators=[username_validator],
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Имя',
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Фамилия',
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Емейл',
    )
    role = models.CharField(
        choices=ROLES,
        max_length=25, default=USER,
        verbose_name='Роль пользователя',
    )
    bio = models.TextField(
        max_length=500,
        blank=True,
    )
    confirmation_code = models.CharField(
        max_length=100,
        verbose_name='Код подтверждения',
    )

    REQUIRED_FIELDS = ['email']
    USERNAME_FIELDS = 'email'

    def __str__(self):
        return str(self.username)

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_user(self):
        return self.role == USER
