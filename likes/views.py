from django.shortcuts import render, redirect
from django.views.generic.base import View

from likes.models import BlogLikes
from main.models import Published
from users.models import Users


class AddLikeView(View):
    def post(self, request, *args, **kwargs):
        blog_post_id = int(request.POST.get('blog_post_id'))
        user_id = int(request.POST.get('user_id'))
        url_from = request.POST.get('url_from')

        user_inst = Users.objects.get(id=user_id)
        blog_post_inst = Published.objects.get(id=blog_post_id)

        try:
            blog_like_inst = BlogLikes.objects.get(blog_post=blog_post_inst, liked_by=user_inst)
        except Exception as e:
            blog_like = BlogLikes(blog_post=blog_post_inst, liked_by=user_inst, like=True)
            blog_like.save()
        return redirect(url_from)


class RemoveLikeView(View):
    def post(self, request, *args, **kwargs):
        blog_likes_id = int(request.POST.get('blog_likes_id'))
        url_from = request.POST.get('url_from')

        blog_like = BlogLikes.objects.get(id=blog_likes_id)
        blog_like.delete()

        return redirect(url_from)
