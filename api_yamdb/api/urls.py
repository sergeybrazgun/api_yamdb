from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CommentViewSet, TitleViewSet, GenreViewSet,
                    CategoryViewSet, SignUpView, TokenObtainView, UserViewSet, ReviewViewSet)


app_name = 'api'

router = DefaultRouter()
router.register('api/v1/titles', TitleViewSet)
router.register('api/v1/genres', GenreViewSet)
router.register('api/v1/categories', CategoryViewSet)
router.register(r'api/v1/titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router.register(r'api/v1/titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                r'/comments', CommentViewSet, basename='comments')
router.register('api/v1/users', UserViewSet)


urlpatterns = [
    path('api/v1/auth/signup/', SignUpView.as_view()),
    path('api/v1/auth/token/', TokenObtainView.as_view()),
    path('', include(router.urls))
]
