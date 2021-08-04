from django import template

from likes.models import BlogLikes

register = template.Library()


@register.filter(name='is_liked_bool')
@register.simple_tag(takes_context=True)
def is_liked(context, blog_post_id):
    request = context['request']
    try:
        blog_likes = BlogLikes.objects.get(blog_post_id=blog_post_id, liked_by=request.user.id).like
    except Exception as e:
        blog_likes = False
    return blog_likes


@register.filter(name='likes_counter')
@register.simple_tag()
def count_likes(blog_post_id):
    return BlogLikes.objects.filter(blog_post_id=blog_post_id, like=True).count()


@register.filter(name='blog_likes_id')
@register.simple_tag(takes_context=True)
def blog_likes_id(context, blog_post_id):
    request = context['request']
    return BlogLikes.objects.get(blog_post_id=blog_post_id, liked_by=request.user.id).id
