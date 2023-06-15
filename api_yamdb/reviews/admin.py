from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Category, Genre, GenreTitle, Title, User


class TitleResource(resources.ModelResource):

    class Meta:
        model = Title


class TitleAdmin(ImportExportModelAdmin):
    resource_classes = [TitleResource]


class CategoryResource(resources.ModelResource):

    class Meta:
        model = Category


class CategoryAdmin(ImportExportModelAdmin):
    resource_classes = [CategoryResource]


class GenreResource(resources.ModelResource):

    class Meta:
        model = Genre


class GenreAdmin(ImportExportModelAdmin):
    resource_classes = [GenreResource]


class GenreResource(resources.ModelResource):

    class Meta:
        model = Genre


class GenreAdmin(ImportExportModelAdmin):
    resource_classes = [GenreResource]


class GenreTitleResource(resources.ModelResource):

    class Meta:
        model = GenreTitle


class GenreTitleAdmin(ImportExportModelAdmin):
    resource_classes = [GenreTitleResource]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(GenreTitle, GenreTitleAdmin)
admin.site.register(User)
