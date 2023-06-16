
from django.shortcuts import get_object_or_404
from rest_framework import (permissions,
                            viewsets,
                            )
from rest_framework.exceptions import ParseError
from rest_framework.pagination import LimitOffsetPagination
from reviews.models import (Review,
                            Title,
                            )

from api.permissions import IsAuthorOrModeratorOrAdminOrReadOnly
from api.serializers import (ReviewSerializer,
                             CommentSerializer,
                             )
from django.shortcuts import render
from rest_framework import viewsets
from reviews.models import Category, Genre, GenreTitle, Title

from .serializers import (CategorySerializer, GenreSerializer,
                          GenreTitleSerializer, TitleSerializer)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [
        IsAuthorOrModeratorOrAdminOrReadOnly,
        permissions.IsAuthenticatedOrReadOnly
    ]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        new_queryset = title.reviews.all()
        return new_queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        if Review.objects.filter(
            title=title,
            author=self.request.user
        ).exists():
            raise ParseError
        serializer.save(
            author=self.request.user, title=title
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [
        IsAuthorOrModeratorOrAdminOrReadOnly,
        permissions.IsAuthenticatedOrReadOnly
    ]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id'),
        )
        new_queryset = review.comments.all()
        return new_queryset

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id'),
        )
        serializer.save(
            author=self.request.user, review=review
        )

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

