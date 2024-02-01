from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import (RegexValidator,
                                    MaxValueValidator,
                                    MinValueValidator)
from .constants import (
    USER_ROLE, MODERATOR_ROLE, ADMIN_ROLE,
    MAX_LENGTH_USERNAME, MAX_LENGTH_NAME,
    MAX_LENGTH_EMAIL, MAX_LENGTH_ROLE,
)
from .validators import year_validator, validate_username

CHOICES = (
    (USER_ROLE, 'User'), (MODERATOR_ROLE, 'Moderator'), (ADMIN_ROLE, 'Admin')
)
SCORE_CHOICES = (
    (1, 'Полный провал'),
    (2, 'Ужасно'),
    (3, 'Плохо'),
    (4, 'Ниже среднего'),
    (5, 'На один раз'),
    (6, 'Выше среднего'),
    (7, 'Очень хорошо'),
    (8, 'Отлично'),
    (9, 'Потрясающе'),
    (10, 'Восторг'),
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


class Review(models.Model):
    title = models.ForeignKey(Title,
                              on_delete=models.CASCADE,
                              related_name='reviews')
    text = models.TextField('Отзыв')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='reviews')
    score = models.IntegerField('Оценка',
                                choices=SCORE_CHOICES,
                                validators=[MinValueValidator(1),
                                            MaxValueValidator(10)])
    pub_date = models.DateTimeField('Дата добавления',
                                    auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review_by_author'
            ),]

    def __str__(self):
        return f'Отзыв на "{self.title}" от {self.author.username}'


class Comment(models.Model):
    review = models.ForeignKey(Review,
                               on_delete=models.CASCADE,
                               related_name='comments')
    text = models.TextField('Комментарий')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='comments')
    pub_date = models.DateTimeField('Дата добавления',
                                    auto_now_add=True,
                                    db_index=True)

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Коментарии'

    def __str__(self):
        return self.text
