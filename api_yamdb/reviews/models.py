from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxLengthValidator

from .validators import year_validator

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
    # is_verified = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return self.username


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Имя жанра',
        null=False,
        blank=False,
        unique=True,
        max_length=256,
    )
    slug = models.SlugField(
        verbose_name='Слаг жанра',
        unique=True,
        max_length=50,
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(
        verbose_name='Имя категории',
        null=False,
        blank=False,
        unique=True,
        max_length=256,
    )
    slug = models.SlugField(
        verbose_name='Слаг категории',
        unique=True,
        max_length=50,
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название произведения',
        null=False,
        blank=False,
        max_length=256
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='Год выхода',
        null=False,
        blank=False,
        validators=[year_validator]
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        verbose_name='Жанр произведения',
        blank=True
    )
    description = models.CharField(
        verbose_name='Описание произведения',
        max_length=256,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Жанр',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
    )

    class Meta:
        verbose_name = 'Жанры произведений'
        verbose_name_plural = 'Жанры произведений'
