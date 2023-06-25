from django.contrib import admin

from .models import Category, GenreTitle, Title, Review, Comments


admin.site.register(Category, )
admin.site.register(Title, )
admin.site.register(GenreTitle, )
admin.site.register(Comments,)
admin.site.register(Review, )
