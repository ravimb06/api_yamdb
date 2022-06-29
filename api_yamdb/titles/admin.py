from django.contrib import admin

from .models import Category, Genre, Title


class CategoryAdmin(admin.ModelAdmin):
    """Класс Категории для админ панели."""
    list_display = (
        'id',
        'name',
        'slug',
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пустое поле-'


class GenreAdmin(admin.ModelAdmin):
    """Класс Жанра для админ панели"""
    list_display = (
        'id',
        'name',
        'slug',
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пустое поле-'


class TitleAdmin(admin.ModelAdmin):
    """Класс Произведения для админ панели"""
    list_display = (
        'id',
        'name',
        'description',
        'year',
        'category',
    )
    search_fields = ('name',)
    list_filter = ('category',)
    empty_value_display = '-пусто-'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
