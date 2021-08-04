from django.contrib import admin

from likes.models import BlogLikes


@admin.register(BlogLikes)
class BlogLikesAdmin(admin.ModelAdmin):
    autocomplete_fields = ['liked_by', 'blog_post']
    list_display = ('blog_post', 'liked_by', 'like', 'created')
