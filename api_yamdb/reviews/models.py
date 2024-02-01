from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import (RegexValidator,
                                    MaxValueValidator,
                                    MinValueValidator)
from .constants import (
    USER_ROLE, MODERATOR_ROLE, ADMIN_ROLE,
    MAX_LENGTH_USERNAME, MAX_LENGTH_NAME,
    MAX_LENGTH_EMAIL, MAX_LENGTH_ROLE,
    MAX_LENGTH_TITLE_NAME, MAX_LENGTH_SLUG,
    MAX_LENGTH_TITLE_DESCRIPTION,
    MAX_LENGTH_GENRE_CATEGORY_NAME,
    SCORE_CHOICES
)
from .validators import year_validator, validate_username

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


class ReviewCommentBaseModel(models.Model):
    text = models.TextField('Текст')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True)

    class Meta:
        abstract = True


class GenreCategoryBaseModel(models.Model):
    name = models.CharField(
        null=False,
        blank=False,
        unique=True,
        max_length=MAX_LENGTH_GENRE_CATEGORY_NAME,
    )
    slug = models.SlugField(
        unique=True,
        max_length=MAX_LENGTH_SLUG,
    )

    class Meta:
        abstract = True


class Genre(GenreCategoryBaseModel):
    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Category(GenreCategoryBaseModel):
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
        max_length=MAX_LENGTH_TITLE_NAME
    )
    year = models.SmallIntegerField(
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
        related_name='genre',
        verbose_name='Жанр произведения',
        blank=True
    )
    description = models.CharField(
        verbose_name='Описание произведения',
        max_length=MAX_LENGTH_TITLE_DESCRIPTION,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(ReviewCommentBaseModel):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews')
    score = models.PositiveSmallIntegerField(
        'Оценка',
        choices=SCORE_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(10)])

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


class Comment(ReviewCommentBaseModel):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments')

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Коментарии'

    def __str__(self):
        return self.text
