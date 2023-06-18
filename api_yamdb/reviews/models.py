from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from reviews.validators import validate_username


class SampleModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)


class User(AbstractUser):
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
        max_length=150,
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
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        max_length=150,
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
    def is_user(self):
        return self.role == self.USER

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    def __str__(self):
        return self.username


class Review(models.Model):
    '''Модель отзывов.'''
    author = models.ForeignKey(
        User,
        related_name='author_review',
        on_delete=models.CASCADE,
        verbose_name='Автор отзыва',
    )
    title = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='review_title',
        verbose_name='Оцениваемое произведение',
    )
    text = models.TextField('Текст отзыва')
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
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
        return self.text[:10]


class Comments(models.Model):
    '''Модель комментариев.'''
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
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ['-pub_date']

    def __str__(self) -> str:
        return self.text[:10]


class Category(models.Model):
    name = models.CharField(
        'название категории', max_length=256)
    slug = models.SlugField('слаг категории', max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категории'
        verbose_name_plural = 'Категория'
        ordering = ['slug']


class Genre(models.Model):
    name = models.CharField('название жанра', max_length=256)
    slug = models.SlugField('слаг категории', max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['name']


class Title(models.Model):
    name = models.CharField('имя произведения', max_length=256)
    year = models.IntegerField('год выхода',
                               validators=[
                                   MinValueValidator(
                                       1900, message='До 1900ого года никто ничего не придумал'),
                                   MaxValueValidator(2023, message='Не надо добавлять произведения из будущего')],)
    category = models.ForeignKey(Category,
                                 related_name='titles',
                                 null=True,
                                 verbose_name='категория',
                                 on_delete=models.SET_NULL)
    genre = models.ManyToManyField(
        Genre, through='GenreTitle', verbose_name='жанр')

    def __str__(self):
        return f'{self.name} ({self.year})'

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['name']


class GenreTitle(models.Model):
    title_id = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre_id = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title_id} ({self.genre_id})'

    class Meta:
        verbose_name = 'Связь Жанров и Произведений'
        verbose_name_plural = 'Связь Жанров и Произведений'
