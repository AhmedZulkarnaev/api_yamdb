from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

from .validator import validate_username
from .constants import (
    USER_ROLE, MODERATOR_ROLE, ADMIN_ROLE,
    MAX_LENGTH_USERNAME, MAX_LENGTH_NAME,
    MAX_LENGTH_EMAIL, MAX_LENGTH_ROLE,
)

CHOICES = (
    (USER_ROLE, 'User'), (MODERATOR_ROLE, 'Moderator'), (ADMIN_ROLE, 'Admin')
)


class User(AbstractUser):
    username = models.CharField(
        verbose_name='Логин',
        max_length=MAX_LENGTH_USERNAME,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[\w@+.-]+$',
                message="Допустимые символы: '_', '@', '+', '.', '-'"
            ),
            validate_username
        ]
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=MAX_LENGTH_NAME,
        blank=True,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=MAX_LENGTH_NAME,
        blank=True,
    )
    email = models.EmailField(
        verbose_name='Email пользователя',
        max_length=MAX_LENGTH_EMAIL,
        unique=True,
    )
    role = models.CharField(
        max_length=MAX_LENGTH_ROLE,
        verbose_name='Роль',
        choices=CHOICES,
        default=USER_ROLE,
        help_text='Роль пользователя',
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
