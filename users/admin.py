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
    list_display = ('owner', 'user', 'date')
    list_display_links = ('owner',)
    fields = ('owner', 'user')
    search_fields = ('owner', 'date')
    list_filter = ('owner', 'date')
    list_max_show_all = 5
    list_per_page = 10

