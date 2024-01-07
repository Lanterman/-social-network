from django.contrib import admin

from src.users.models import User, Follower, Chat, Message


@admin.register(User)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'slug', 'email', 'num_tel')
    list_display_links = ('id', 'username', 'first_name', 'last_name',)
    fields = ('username', 'first_name', 'last_name', 'slug', 'email', 'num_tel', 'photo',)
    search_fields = ('username', 'first_name', 'last_name', 'slug', 'email')
    list_filter = ('first_name', 'last_name', 'slug', 'email')
    list_max_show_all = 5
    list_per_page = 10
    prepopulated_fields = {'slug': ('username',)}


@admin.register(Follower)
class PostSubscribersAdmin(admin.ModelAdmin):
    list_display = ('follower_id', 'subscription_id', 'date', 'is_checked')
    list_display_links = ('follower_id',)
    fields = ('follower_id', 'subscription_id', 'is_checked')
    search_fields = ('follower_id', 'date', 'is_checked')
    list_filter = ('follower_id', 'date', 'is_checked')
    list_max_show_all = 5
    list_per_page = 10


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    raw_id_fields = ('members',)
    fields = ('members',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'author_id', 'is_readed', 'pub_date')
    list_display_links = ('id', 'author_id')
    fields = ('chat_id', 'author_id', 'message', 'is_readed')
    actions = ['message_true', 'message_false']

    @admin.action(description='Прочитать сообщения')
    def message_true(self, request, queryset):
        queryset.update(is_readed=True)

    @admin.action(description='Отметить как непрочитанные')
    def message_false(self, request, queryset):
        queryset.update(is_readed=False)
