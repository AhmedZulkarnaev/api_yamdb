from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


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
TEXT_LENGTH_STR = 20


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
        return self.text[:TEXT_LENGTH_STR]
