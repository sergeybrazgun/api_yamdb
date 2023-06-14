from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()



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
