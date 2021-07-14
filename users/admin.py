from django.contrib import admin

from users.models import *


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'slug', 'email', 'num_tel')
    list_display_links = ('username', 'first_name', 'last_name',)
    fields = ('username', 'first_name', 'last_name', 'slug', 'email', 'num_tel', 'photo',)
    search_fields = ('username', 'first_name', 'last_name', 'slug', 'email')
    list_filter = ('first_name', 'last_name', 'slug', 'email')
    list_max_show_all = 5
    list_per_page = 10
    ordering = ('first_name', 'last_name',)
    prepopulated_fields = {'slug': ('first_name', 'last_name')}
