import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404

from reviews.models import (Category, Comments, Genre, GenreTitle, Review,
                            Title, User)


def get_reader(file_name: str):
    csv_path = os.path.join(settings.BASE_DIR, 'static/data/', file_name)
    csv_file = open(csv_path, 'r', encoding='utf-8')
    reader = csv.reader(csv_file, delimiter=',')
    return reader


class Command(BaseCommand):

    def handle(self, *args, **options):
        csv_reader = get_reader('category.csv')
        next(csv_reader, None)
        for row in csv_reader:
            obj, created = Category.objects.get_or_create(
                id=row[0],
                name=row[1],
                slug=row[2]
            )
        print('category: импорт завершен')

        csv_reader = get_reader('genre.csv')
        next(csv_reader, None)
        for row in csv_reader:
            obj, created = Genre.objects.get_or_create(
                id=row[0],
                name=row[1],
                slug=row[2]
            )
        print('genre: импорт завершен')

        csv_reader = get_reader('titles.csv')
        next(csv_reader, None)
        for row in csv_reader:
            obj_category = get_object_or_404(Category, id=row[3])
            obj, created = Title.objects.get_or_create(
                id=row[0],
                name=row[1],
                year=row[2],
                category=obj_category
            )
        print('titles: импорт завершен')

        csv_reader = get_reader('genre_title.csv')
        next(csv_reader, None)
        for row in csv_reader:
            obj_genre = get_object_or_404(Genre, id=row[2])
            obj_title = get_object_or_404(Title, id=row[1])
            obj, created = GenreTitle.objects.get_or_create(
                id=row[0],
                genre_id=obj_genre,
                title_id=obj_title
            )
        print('genre_titles: импорт завершен')

        csv_reader = get_reader('users.csv')
        next(csv_reader, None)
        for row in csv_reader:
            obj, created = User.objects.get_or_create(
                id=row[0],
                username=row[1],
                email=row[2],
                role=row[3],
                bio=row[4],
                first_name=row[5],
                last_name=row[6]
            )
        print('users: импорт завершен')

        csv_reader = get_reader('review.csv')
        next(csv_reader, None)
        for row in csv_reader:
            obj_title = get_object_or_404(Title, id=row[1])
            obj_user = get_object_or_404(User, id=row[3])
            obj, created = Review.objects.get_or_create(
                id=row[0],
                title=obj_title,
                text=row[2],
                author=obj_user,
                score=row[4],
                pub_date=row[5]
            )
        print('review: импорт завершен')

        csv_reader = get_reader('comments.csv')
        next(csv_reader, None)
        for row in csv_reader:
            obj_review = get_object_or_404(Review, id=row[1])
            obj_user = get_object_or_404(User, id=row[3])
            obj, created = Comments.objects.get_or_create(
                id=row[0],
                review=obj_review,
                text=row[2],
                author=obj_user,
                pub_date=row[4]
            )
        print('comments: импорт завершен')