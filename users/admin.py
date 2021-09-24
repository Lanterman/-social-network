from django.contrib import admin

from users.models import *


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'slug', 'email', 'num_tel')
    list_display_links = ('username', 'first_name', 'last_name',)
    fields = ('username', 'first_name', 'last_name', 'slug', 'email', 'num_tel', 'friends', 'photo',)
    search_fields = ('username', 'first_name', 'last_name', 'slug', 'email')
    list_filter = ('first_name', 'last_name', 'slug', 'email')
    list_max_show_all = 5
    list_per_page = 10
    prepopulated_fields = {'slug': ('username',)}
    raw_id_fields = ('friends',)


@admin.register(PostSubscribers)
class PostSubscribersAdmin(admin.ModelAdmin):
    list_display = ('owner', 'user', 'date', 'escape')
    list_display_links = ('owner',)
    fields = ('owner', 'user', 'escape')
    search_fields = ('owner', 'date', 'escape')
    list_filter = ('owner', 'date', 'escape')
    list_max_show_all = 5
    list_per_page = 10


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    raw_id_fields = ('members',)
    fields = ('members',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'is_readed', 'pub_date')
    list_display_links = ('id', 'author')
    fields = ('chat', 'author', 'message', 'is_readed')
    actions = ['message_true', 'message_false']

    @admin.action(description='Прочитать сообщения')
    def message_true(self, request, queryset):
        queryset.update(is_readed=True)

    @admin.action(description='Отметить как непрочитанные')
    def message_false(self, request, queryset):
        queryset.update(is_readed=False)
