from django.http import HttpResponse
from django.shortcuts import render
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
    group = Groups.objects.all()[:5]
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


def detail_publish(request, publish_slug):
    return HttpResponse('Запись %s' % publish_slug)


def comments(request):
    return HttpResponse('asdaf')