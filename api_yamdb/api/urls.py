from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import GenreTitleViewSet, TitleViewSet, GenreViewSet, CategoryViewSet


app_name = 'api'

router = DefaultRouter()
router.register('api/v1/titles', TitleViewSet)
router.register('api/v1/genres', GenreViewSet)
router.register('api/v1/categories', CategoryViewSet)
router.register('api/v1/genretitles', GenreTitleViewSet)

urlpatterns = [
    path('',include(router.urls))
]
