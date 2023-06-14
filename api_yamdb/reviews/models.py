from django.contrib.auth import get_user_model

from django.core.validators import MaxValueValidator, MinValueValidator

from django.db import models

User = get_user_model()



class Review(models.Model):
    '''Модель отзывов.'''
    author = models.ForeignKey(
        User,
        related_name='reviews',
        on_delete=models.CASCADE,
        verbose_name='Автор отзыва',
    )
    title = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Оцениваемое произведение',
    )
    text = models.TextField('Текст отзыва')
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )
    score = models.PositiveSmallIntegerField(
        'Оценка произведения',
        validators=[
            MinValueValidator(1, message='Оценка должна быть не меньше 1.'),
            MaxValueValidator(10, message='Оценка должна быть не больше 10.')
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
        'название категории', max_length=30)
    slug = models.SlugField('слаг категории', unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категории'
        verbose_name_plural = 'Категория'
        ordering = ['name']


class Genre(models.Model):
    name = models.CharField('название жанра', max_length=30)
    slug = models.SlugField('слаг категории', unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['name']



class Title(models.Model):
    name = models.CharField('имя произведения', max_length=30)
    year = models.IntegerField('год выхода')
    category = models.ForeignKey(Category, null=True,related_name='titles', verbose_name='категория', on_delete=models.SET_NULL)
    genre = models.ManyToManyField(Genre, through='GenreTitle', verbose_name='жанр')

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

