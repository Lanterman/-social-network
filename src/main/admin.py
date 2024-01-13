from django.contrib import admin

from src.main.models import Publication, Group, Comment, RatingStar, Rating


class AbstractAdmin(admin.ModelAdmin):
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')
    list_filter = ('name',)  # Фильтер справа
    list_max_show_all = 5  # Если больше этого значения экземпляров - появляется кнопка
    list_per_page = 10  # Разбиение на страницы
    ordering = ('-date',)
    prepopulated_fields = {'slug': ('name',)}  # Автозаполнение поля slug с помощью name


@admin.register(Group)
class GroupAdmin(AbstractAdmin):
    ordering = ('-id',)
    list_display = ('id', 'name', 'slug', 'photo')
    fields = ('name', 'slug', 'photo', 'users', 'owner')
    raw_id_fields = ('users',)  # удобная вещь при связях


@admin.register(Publication)
class PublicationAdmin(AbstractAdmin):
    list_display = ('id', 'name', 'slug', 'photo', 'date', 'owner')
    fields = ('name', 'slug', 'biography', 'group', 'photo', 'date', 'owner')
    date_hierarchy = 'date'
    readonly_fields = ('date',)  # делает нередактиремым


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'publication_id', 'users', 'date')
    list_display_links = ('id', 'publication_id', 'users')
    fields = ('biography', 'publication_id', 'users', 'date', 'like')
    search_fields = ('publication_id', 'date', 'users')
    list_filter = ('date', 'users')
    list_max_show_all = 5
    list_per_page = 10
    ordering = ('-date',)
    raw_id_fields = ('publication_id', 'users', 'like')
    date_hierarchy = 'date'
    readonly_fields = ('date',)


@admin.register(RatingStar)
class RatingStarAdmin(admin.ModelAdmin):
    pass


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('publication_id', 'star', 'ip')
