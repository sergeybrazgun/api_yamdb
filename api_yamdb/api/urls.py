from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CommentViewSet, TitleViewSet, GenreViewSet,
                    CategoryViewSet, SignUpView, TokenObtainView,
                    UserViewSet, ReviewViewSet)


app_name = 'api'

router = DefaultRouter()
router.register('titles', TitleViewSet)
router.register('genres', GenreViewSet)
router.register('categories', CategoryViewSet)
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                r'/comments', CommentViewSet, basename='comments')
router.register('users', UserViewSet)


urlpatterns = [
    path('v1/auth/signup/', SignUpView.as_view()),
    path('v1/auth/token/', TokenObtainView.as_view()),
    path('v1/', include(router.urls))
]
