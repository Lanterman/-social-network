from django.contrib import admin

from src.users.models import User, Follower, Chat, Message

# Inline Message model to ChatAdmin (ability to instantiate Message model for ChatAdmin)
class MessageInline(admin.TabularInline):
    model = Message


@admin.register(User)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'slug', 'email', 'num_tel')
    list_display_links = ('id', 'username', 'first_name', 'last_name',)
    fields = ('username', 'first_name', 'last_name', 'slug', 'email', 'num_tel', 'photo', 'hashed_password')
    search_fields = ('username', 'first_name', 'last_name', 'slug', 'email')
    list_filter = ('first_name', 'last_name', 'slug', 'email')
    list_max_show_all = 5
    list_per_page = 10
    prepopulated_fields = {'slug': ('username',)}


@admin.register(Follower)
class FollowerAdmin(admin.ModelAdmin):
    list_display = ('id', 'follower_id', 'subscription_id', 'date', 'is_checked')
    list_display_links = ('follower_id',)
    fields = ('follower_id', 'subscription_id', 'is_checked')
    search_fields = ('follower_id', 'date', 'is_checked')
    list_filter = ('follower_id', 'subscription_id', 'date', 'is_checked')
    list_max_show_all = 5
    list_per_page = 10
    actions = ["confirm_checking_followers", "unconfirm_checking_followers"]

    @admin.action(description='Confirm checking followers')
    def confirm_checking_followers(self, request, queryset):
        queryset.update(is_checked=True)

    @admin.action(description='Unconfirm checking followers')
    def unconfirm_checking_followers(self, request, queryset):
        queryset.update(is_checked=False)


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    raw_id_fields = ('members',)
    fields = ('members',)
    inlines = [MessageInline]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'author_id', 'is_readed', 'pub_date')
    list_display_links = ('id', 'author_id')
    fields = ('chat_id', 'author_id', 'message', 'is_readed')
    actions = ['message_true', 'message_false']

    @admin.action(description='Read messages')
    def message_true(self, request, queryset):
        queryset.update(is_readed=True)

    @admin.action(description='Mark as unread')
    def message_false(self, request, queryset):
        queryset.update(is_readed=False)
