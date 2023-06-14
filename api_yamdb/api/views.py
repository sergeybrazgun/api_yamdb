from django.shortcuts import render
from rest_framework import viewsets
from reviews.models import Category, Genre, GenreTitle, Title

from .serializers import (CategorySerializer, GenreSerializer,
                          GenreTitleSerializer, TitleSerializer)


class TitleViewSet(viewsets.ModelViewSet):
    queryset =Title.objects.all()
    serializer_class = TitleSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset =Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset =Category.objects.all()
    serializer_class = CategorySerializer


class GenreTitleViewSet(viewsets.ModelViewSet):
    queryset =GenreTitle.objects.all()
    serializer_class = GenreTitleSerializer
