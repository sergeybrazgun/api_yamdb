from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .abstract_models import PubDateAbstractModel
from reviews.validators import validate_username

MAX_LENGTH = 150
MAX_LENGTH_2 = 256
MAX_LENGTH_3 = 50
ON_PAGE = 10


class SampleModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)


class User(AbstractUser):
    """Модель пользователя"""
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'

    ROLE_CHOICES = (
        (USER, 'Пользователь'),
        (ADMIN, 'Админ'),
        (MODERATOR, 'Модератор'),
    )

    username = models.CharField(
        validators=[validate_username],
        max_length=MAX_LENGTH,
        unique=True,
        blank=False,
        null=False
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        blank=False,
        null=False
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=USER,
        blank=True
    )
    bio = models.TextField(
        blank=True,
    )
    first_name = models.CharField(
        max_length=MAX_LENGTH,
        blank=True
    )
    last_name = models.CharField(
        max_length=MAX_LENGTH,
        blank=True
    )
    confirmation_code = models.CharField(
        max_length=255,
        null=True,
        blank=False,
        default='XXXX'
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    def __str__(self):
        return self.username


class Category(models.Model):
    """Модель категорий"""
    name = models.CharField(
        'название категории', max_length=MAX_LENGTH_2)
    slug = models.SlugField('слаг категории',
                            max_length=MAX_LENGTH_3, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категории'
        verbose_name_plural = 'Категория'
        ordering = ['slug']


class Genre(models.Model):
    """Модель жанров"""
    name = models.CharField('название жанра', max_length=MAX_LENGTH_2)
    slug = models.SlugField('слаг категории',
                            max_length=MAX_LENGTH_3, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['name']


class Title(models.Model):
    """Модель произведений"""
    name = models.CharField('имя произведения', max_length=MAX_LENGTH_2)
    year = models.IntegerField('год выхода',
                               validators=[
                                   MinValueValidator(
                                       1900,
                                       message='Не надо'
                                       'добовлять произведения ранее 1900-го года'),
                                   MaxValueValidator(
                                       2023,
                                       message='Не надо'
                                       'добавлять произведения из будущего')],)
    category = models.ForeignKey(Category,
                                 related_name='titles',
                                 null=True,
                                 verbose_name='категория',
                                 on_delete=models.SET_NULL)
    genre = models.ManyToManyField(
        Genre, through='GenreTitle', verbose_name='жанр')
    rating = models.PositiveSmallIntegerField(
        verbose_name='Рейтинг',
        null=True,
        default=None,
        validators=[
            MinValueValidator(
                1, message='Оценка должна быть не меньше 1.'),
            MaxValueValidator(
                10, message='Оценка должна быть не больше 10.')
        ],
    )
    description = models.TextField(
        verbose_name='Описание',
        null=True,
        blank=True
    )

    def __str__(self):
        return f'{self.name} ({self.year})'

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['name']


class Review(PubDateAbstractModel):
    """Модель отзывов."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='review_title',
        verbose_name='Оцениваемое произведение',
    )
    text = models.TextField('Текст отзыва')
    author = models.ForeignKey(
        User,
        related_name='author_review',
        on_delete=models.CASCADE,
        verbose_name='Автор отзыва',
    )
    score = models.PositiveSmallIntegerField(
        'Оценка произведения',
        validators=[
            MinValueValidator(
                1, message='Оценка должна быть не меньше 1.'),
            MaxValueValidator(
                10, message='Оценка должна быть не больше 10.')
        ],
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'], name='unique follow',
            )
        ]
        ordering = ['-pub_date']

    def __str__(self) -> str:
        return self.text[:ON_PAGE]


class Comments(PubDateAbstractModel):
    """Модель комментариев."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария',
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE, related_name='comments',
        verbose_name='Комментируемый отзыв'
    )
    text = models.TextField('Текст комметария')

    class Meta:
        ordering = ['-pub_date']

    def __str__(self) -> str:
        return self.text[:ON_PAGE]


class GenreTitle(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} ({self.genre})'

    class Meta:
        verbose_name = 'Связь Жанров и Произведений'
        verbose_name_plural = 'Связь Жанров и Произведений'
