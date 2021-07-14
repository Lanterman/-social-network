from django.contrib import admin

from main.models import *


class AbstractAdmin(admin.ModelAdmin):
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')
    # list_editable = ['name']  # Можно редактировать на странице изменений
    list_filter = ('name',)  # Фильтер справа
    list_max_show_all = 5  # Если больше этого значения экземпляров - появляется кнопка
    list_per_page = 10  # Разбиение на страницы
    ordering = ('-id',)
    prepopulated_fields = {'slug': ('name',)}  # Автозаполнение поля slug с помощью name


@admin.register(Groups)
class GroupsAdmin(AbstractAdmin):
    list_display = ('id', 'name', 'slug', 'photo', 'num_pub')
    fields = ('name', 'slug', 'photo', 'num_pub', 'users', 'published')
    raw_id_fields = ('published', 'users')  # удобная вещь при связях


@admin.register(Published)
class PublishedAdmin(AbstractAdmin):
    list_display = ('id', 'name', 'slug', 'photo', 'date', 'like', 'dislike')
    fields = ('name', 'slug', 'biography', 'photo', 'date', 'like', 'dislike')
    date_hierarchy = 'date'
    readonly_fields = ('date', 'like', 'dislike')  # делает нередактиремым
    actions = ['not_dislike']

    @admin.action(description='Анилировать лайки и дизлайки')
    def not_dislike(self, request, queryset):
        rows = queryset.update(dislike=0, like=0)
        if rows == 1:
            messages = 'Лайки и дизлайки 1 публикации были анулированы'
        else:
            messages = 'Лайки и дизлайки %s публикации были анулированы' % rows
        self.message_user(request, messages)


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'published', 'users', 'date', 'like')
    list_display_links = ('id', 'published', 'users')
    fields = ('biography', 'published', 'users', 'date', 'like')
    search_fields = ('published', 'date', 'users')
    list_filter = ('date', 'users')
    list_max_show_all = 5
    list_per_page = 10
    ordering = ('-date',)
    raw_id_fields = ('published', 'users')
    date_hierarchy = 'date'
    readonly_fields = ('date', 'like')
    actions = ['not_like']

    @admin.action(description='Анилировать лайки')
    def not_like(self, request, queryset):
        rows = queryset.update(like=0)
        if rows == 1:
            message_bit = "дизлайки 1 публикации была анулированы"
        else:
            message_bit = "Дизлайки %s публикаций были анулированы" % rows
        self.message_user(request, message_bit)
