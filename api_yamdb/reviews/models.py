from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.conf import settings

from users.models import User


class BaseModel(models.Model):
    """Абстрактная модель для Жанров и Категорий"""
    name = models.CharField('Название', max_length=settings.LEN_FOR_NAME)
    slug = models.SlugField('Слаг', unique=True,
                            max_length=settings.LEN_FOR_SLUG)

    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self):
        return self.name[:settings.MAX_TEXT]


class Genre(BaseModel):
    """Жанр произведений"""

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Category(BaseModel):
    """Категории (типы) произведений («Фильмы», «Книги», «Музыка»)."""

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Title(models.Model):
    """
    Произведения, к которым пишут отзывы (определённый фильм,
    книга или песенка).
    """
    def validate_year(value):
        if value > timezone.now().year:
            raise ValidationError(
                'Год выхода не может быть больше текущего года.'
            )

    name = models.CharField('Название', max_length=settings.LEN_FOR_NAME)
    year = models.IntegerField('Год выхода', validators=[validate_year])
    description = models.TextField('Описание', blank=True)
    genre = models.ManyToManyField(
        Genre, through='TitleGenre', verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='titles',
        verbose_name='Категория'
    )

    class Meta:
        ordering = ('-year',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return f'{self.name} ({self.year})'


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


class BaseReviewComment(models.Model):
    """Абстрактная модель для Отзывов и Комментариев"""
    text = models.TextField(
        verbose_name='текст',
        max_length=settings.MAX_LENGTH,
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
    """Отзывы на произведения"""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
    )
    score = models.IntegerField(
        verbose_name='Оценка',
        validators=[
            MinValueValidator(settings.MIN_SCORE),
            MaxValueValidator(settings.MAX_SCORE),
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
        return self.text[:settings.MAX_TEXT]


class Comment(BaseReviewComment):
    """Комментарии к отзывам"""
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
        return self.text[:settings.MAX_TEXT]
