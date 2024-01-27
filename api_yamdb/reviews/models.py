from django.db import models
from django.core.validators import MaxLengthValidator
from django.contrib.auth.models import AbstractUser

CHOICES = [('user', 'User'), ('moderator', 'Moderator'), ('admin', 'Admin')]


class CustomUser(AbstractUser):
    username = models.CharField(
        verbose_name='Логин',
        max_length=150,
        unique=True,
        blank=False,
        null=False,
        validators=[MaxLengthValidator(150)]
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        blank=True,
        validators=[MaxLengthValidator(150)]
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        blank=True,
        validators=[MaxLengthValidator(150)]
    )
    email = models.EmailField(
        verbose_name='Email пользователя',
        max_length=254,
        unique=True,
        validators=[MaxLengthValidator(254)]
    )
    role = models.CharField(
        max_length=15,
        verbose_name='Роль',
        choices=CHOICES,
        default='user',
        help_text='Роль пользователя',
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )
    is_verified = models.BooleanField(default=False)
    confirmation_code = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return self.username
