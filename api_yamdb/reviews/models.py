from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User
from api_yamdb.settings import MIN_SCORE, MAX_SCORE, MAX_LENGTH, MAX_TEXT


class Genre(models.Model):
    """Жанр произведений"""
    name = models.CharField('Название', max_length=256)
    slug = models.SlugField('Слаг', unique=True, max_length=50)

    def __str__(self):
        return self.name


class Category(models.Model):
    """Категории (типы) произведений («Фильмы», «Книги», «Музыка»)."""
    name = models.CharField('Название', max_length=256)
    slug = models.SlugField('Слаг', unique=True, max_length=50)

    def __str__(self):
        return self.name


class Title(models.Model):
    """
    Произведения, к которым пишут отзывы (определённый фильм,
    книга или песенка).
    """
    name = models.CharField('Название', max_length=256)
    year = models.IntegerField('Год выхода')
    description = models.TextField('Описание', blank=True, null=True)
    genre = models.ManyToManyField(
        Genre, through='TitleGenre', verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='title',
        verbose_name='Категория'
    )


class TitleGenre(models.Model):
    """Определение нескольких жанров произведений"""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Жанр'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'genre'],
                name='unique_title_genre_pair'
            )
        ]

    def __str__(self):
        return f'{self.title} {self.genre}'


class BaseReviewComment(models.Model):
    text = models.TextField(
        verbose_name='текст',
        max_length=MAX_LENGTH,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        abstract = True


class Review(BaseReviewComment):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
    )
    score = models.IntegerField(
        verbose_name='Оценка',
        validators=[
            MinValueValidator(MIN_SCORE),
            MaxValueValidator(MAX_SCORE),
        ],
        error_messages={
            'unique': 'Оценка от 1 до 10'
        }
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        default_related_name = 'reviews'
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author',),
                name='unique_review'
            )
        ]
        ordering = ('pub_date',)

    def __str__(self):
        return self.text[:MAX_TEXT]


class Comment(BaseReviewComment):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Ревью',
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'
        ordering = ('-pub_date',)

    def __str__(self):
        #return str(self.author)
        return self.text[:MAX_TEXT]
