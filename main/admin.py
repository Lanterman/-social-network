from django.contrib import admin

from main.models import *


class AbstractAdmin(admin.ModelAdmin):
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')
    list_filter = ('name',)  # Фильтер справа
    list_max_show_all = 5  # Если больше этого значения экземпляров - появляется кнопка
    list_per_page = 10  # Разбиение на страницы
    ordering = ('-date',)
    prepopulated_fields = {'slug': ('name',)}  # Автозаполнение поля slug с помощью name


@admin.register(Groups)
class GroupsAdmin(AbstractAdmin):
    ordering = ('-id',)
    list_display = ('id', 'name', 'slug', 'photo')
    fields = ('name', 'slug', 'photo', 'users', 'owner')
    raw_id_fields = ('users',)  # удобная вещь при связях


@admin.register(Published)
class PublishedAdmin(AbstractAdmin):
    list_display = ('id', 'name', 'slug', 'photo', 'date', 'owner')
    fields = ('name', 'slug', 'biography', 'group', 'photo', 'date', 'owner')
    date_hierarchy = 'date'
    readonly_fields = ('date',)  # делает нередактиремым


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'published', 'users', 'date')
    list_display_links = ('id', 'published', 'users')
    fields = ('biography', 'published', 'users', 'date', 'like')
    search_fields = ('published', 'date', 'users')
    list_filter = ('date', 'users')
    list_max_show_all = 5
    list_per_page = 10
    ordering = ('-date',)
    raw_id_fields = ('published', 'users', 'like')
    date_hierarchy = 'date'
    readonly_fields = ('date',)


@admin.register(RatingStar)
class RatingStarAdmin(admin.ModelAdmin):
    pass


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('published', 'star', 'ip')
