from django.conf import settings
from django.db import models
from django.utils import timezone

from main.models import Published


class BlogLikes(models.Model):
    blog_post = models.ForeignKey(Published, on_delete=models.SET_NULL, null=True, verbose_name='Публикация')
    liked_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name='Поставить лайк')
    like = models.BooleanField('Like', default=False)
    created = models.DateTimeField('Дата и время', default=timezone.now)

    def __str__(self):
        return f'{self.liked_by}: {self.blog_post} {self.like}'

    class Meta:
        verbose_name = 'Blog Like'
        verbose_name_plural = 'Blog Likes'


# {% include 'likes/add_like_blog.html' with blog_post_id=published.id %}