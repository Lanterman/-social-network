from django.contrib import admin

from src.main.models import Publication, Groups, Comments, RatingStar, Rating


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


@admin.register(Publication)
class PublicationAdmin(AbstractAdmin):
    list_display = ('id', 'name', 'slug', 'photo', 'date', 'owner')
    fields = ('name', 'slug', 'biography', 'group', 'photo', 'date', 'owner')
    date_hierarchy = 'date'
    readonly_fields = ('date',)  # делает нередактиремым


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'publication', 'users', 'date')
    list_display_links = ('id', 'publication', 'users')
    fields = ('biography', 'publication', 'users', 'date', 'like')
    search_fields = ('publication', 'date', 'users')
    list_filter = ('date', 'users')
    list_max_show_all = 5
    list_per_page = 10
    ordering = ('-date',)
    raw_id_fields = ('publication', 'users', 'like')
    date_hierarchy = 'date'
    readonly_fields = ('date',)


@admin.register(RatingStar)
class RatingStarAdmin(admin.ModelAdmin):
    pass


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('published', 'star', 'ip')
