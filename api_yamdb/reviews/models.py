from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from django.db import models

from users.models import User
from .validators import year_validator


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название категории',
        help_text='Категория произведения',
        db_index=True
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Часть пути',
        help_text='Часть адреса страницы категории'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return str(self.name)


class Genre(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название жанра',
        help_text='Жанр произведения',
        db_index=True
    )
    slug = models.SlugField(
        unique=True,
        validators=[RegexValidator(
            regex='^[-a-zA-Z0-9_]+$',
            message='Invlaid slug, only ^[-a-zA-Z0-9_]+$')],
        verbose_name='Часть пути',
        help_text='Часть адреса страницы жанра'
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self) -> str:
        return str(self.name)


class Title(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название произведения',
        db_index=True
    )
    year = models.IntegerField(
        verbose_name='Дата создания произведения',
        db_index=True,
        validators=[year_validator],
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True,
        verbose_name='Категории'
    )
    description = models.TextField(
        verbose_name='Описание произведения',
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр произведения'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self) -> str:
        return str(self.name)


class Review(models.Model):
    text = models.TextField(
        help_text='Текст нового отзыва',
        verbose_name='Текст отзыва'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публицации',
        auto_now_add=True,
        db_index=True
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='author_reviews',
        verbose_name='Автор',
    )
    score = models.IntegerField(
        verbose_name='Рейтинг из ревью',
        db_index=True,
        validators=(
            MinValueValidator(1, 'Минимум 1',),
            MaxValueValidator(10, 'Максимум 10',)
        )
    )
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='reviews',
        help_text='Произведение, к которому относится отзыв',
        db_index=True
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_author_title')
        ]

    def __str__(self):
        return self.text[:20]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        verbose_name='Ссылка на пост',
        on_delete=models.CASCADE,
        related_name='comments',
        help_text='Ссылка на пост, к которому оставлен комментарий',
        null=True,
        blank=True,
    )

    author = models.ForeignKey(
        User,
        verbose_name='Автор комментария',
        on_delete=models.CASCADE,
        related_name='comments',
        help_text='Ссылка на автора комментария ',
        db_index=True
    )
    text = models.TextField(
        verbose_name='Текст коммнтария',
        help_text='Текст нового комментария',
    )
    pub_date = models.DateTimeField(
        verbose_name='дата и время публикации комментария',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:15]
