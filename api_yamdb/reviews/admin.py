from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Category, Genre, GenreTitle, Title, User, Review, Comments, ReviewImport


class TitleResource(resources.ModelResource):

    class Meta:
        model = Title


class TitleAdmin(ImportExportModelAdmin):
    resource_classes = [TitleResource]

# class ReviewResource(resources.ModelResource):

#     class Meta:
#         model = Review
#         exclude = ('pub_date')


# class ReviewAdmin(ImportExportModelAdmin):
#     resource_classes = [ReviewResource]

# class CommentResource(resources.ModelResource):

#     class Meta:
#         model = Comments
#         exclude = ('pub_date')

# class CommentAdmin(ImportExportModelAdmin):
#     resource_classes = [CommentResource]


class UserResource(resources.ModelResource):

    class Meta:
        model = User


class UserAdmin(ImportExportModelAdmin):
    resource_classes = [UserResource]


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
admin.site.register(User, UserAdmin)
admin.site.register(Comments,)
# admin.site.register(Review, )


# обслуживание импорта
import csv
from .forms import ReviewImportForm
from django.urls import path
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

# отображает панель для модели BookImport
@admin.register(ReviewImport)
class ReviewImportAdmin(admin.ModelAdmin):
    list_display = ('csv_file',)

# отображает панель для модели Review и метод для импорта
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'text','pub_date', 'score',)
    
    # даем django(urlpatterns) знать
    # о существовании страницы с формой
    # иначе будет ошибка
    def get_urls(self):
        urls = super().get_urls()
        urls.insert(-1, path('csv-upload/', self.upload_csv))
        return urls

    # если пользователь открыл url 'csv-upload/'
    # то он выполнит этот метод
    # который работает с формой
    def upload_csv(self, request):
        if request.method == 'POST':
            form = ReviewImportForm(request.POST, request.FILES)
            if form.is_valid():
                # сохраняем загруженный файл и делаем запись в базу
                form_object = form.save()
                # обработка csv файла
                with form_object.csv_file.open('r',encoding='utf8') as csv_file:
                    rows = csv.reader(csv_file, delimiter=',')
                    if next(rows) != ['title', 'author', 'text','pub_date', 'score',]:
                        # обновляем страницу пользователя
                        # с информацией о какой-то ошибке
                        messages.warning(request, 'Неверные заголовки у файла')
                        return HttpResponseRedirect(request.path_info)
                    for row in rows:
                        print(row[2])
                        # добавляем данные в базу
                        Review.objects.update_or_create(
                            name=row[0],
                            author=row[1],
                            publish_date=row[2]
                        )
                # конец обработки файлы
                # перенаправляем пользователя на главную страницу
                # с сообщением об успехе
                url = reverse('admin:index')
                messages.success(request, 'Файл успешно импортирован')
                return HttpResponseRedirect(url)
        form = ReviewImportForm()
        return render(request, 'admin/csv_import_page.html', {'form': form})
