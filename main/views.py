from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from main.models import *

menu = [
    {'name': 'Главная страница', 'url': 'home'},
    {'name': 'Новости', 'url': 'news'},
    {'name': 'Сообщения', 'url': 'messages'},
    {'name': 'Друзья', 'url': 'friends'},
    {'name': 'Группы', 'url': 'groups'}
]


def news(request):
    public = Published.objects.all()
    group = Groups.objects.all()
    context = {'title': 'Новости', 'public': public, 'menu': menu, 'group': group}
    return render(request, 'main/index.html', context)


def home(request):
    context = {'title': 'Главная страница', 'menu': menu}
    return render(request, 'main/home.html', context)


def messages(request):
    return HttpResponse('Мои сообщения')


def friends(request):
    return HttpResponse('Список друзей')


def groups(request):
    return HttpResponse('Список групп')


def detail_group(request, group_slug):
    return HttpResponse('Группа %s' % group_slug)


class DetailPublish(DetailView):
    model = Published
    slug_url_kwarg = 'publish_slug'
    template_name = 'main/detail_publish.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        return context


# class CommentsPublished(DetailView):
#     model = Published
#     slug_url_kwarg = 'publish_slug'
#     template_name = 'main/comments.html'
#     paginator = 2
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['menu'] = menu
#         return context


def comments(request, publish_slug):
    public = Published.objects.get(slug=publish_slug)
    comment = public.comments_set.all()
    paginator = Paginator(comment, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'menu': menu, 'public': public, 'comment': comment, 'page_obj': page_obj}
    return render(request, 'main/comments.html', context)
