from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView
from django.views.generic.detail import SingleObjectMixin

from main.form import AddCommentForm
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


class DetailGroup(DetailView):
    template_name = 'main/detail_group.html'
    slug_url_kwarg = 'group_slug'
    model = Groups

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        return context


class DetailPublish(DetailView):
    model = Published
    slug_url_kwarg = 'publish_slug'
    template_name = 'main/detail_publish.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        return context


class PublishedCommentsView(SingleObjectMixin, ListView):
    template_name = 'main/comments.html'
    paginate_by = 3
    slug_url_kwarg = 'publish_slug'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Published.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['published'] = self.object
        context['title'] = 'Комментарии'
        return context

    def get_queryset(self):
        return self.object.comments_set.all().select_related('users')  # Жадный запрос


# def comments(request, publish_slug):
#     public = Published.objects.get(slug=publish_slug)
#     comment = public.comments_set.all()
#     paginator = Paginator(comment, 3)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     context = {'menu': menu, 'public': public, 'page_obj': page_obj}
#     return render(request, 'main/comments.html', context)


# def add_user_comment_view(request, users_slug):
#     user1 = Published.objects.get(slug=users_slug)
#     if request.user.is_authenticated:
#         form = AddCommentForm()
#         if request.method == 'POST':
#             form = AddCommentForm(request.POST)
#             if form.is_valid():
#                 form.save()
#
#             context = {'menu': menu, 'title': 'Добавить комментарий', 'form': form}
#             return render(request, 'main/add_comment.html', context)
#         return HttpResponse('Необходимо войти в систему!')


class AddCommentView(LoginRequiredMixin, CreateView):  # Форматировать: пользователь и публикация выбиралась автоматом!
    slug_url_kwarg = 'users_slug'
    login_url = '/users/login/'
    form_class = AddCommentForm
    template_name = 'main/add_comment.html'
    success_url = reverse_lazy('news')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавить Комментарий'
        context['menu'] = menu
        return context

# def add_comment(request, publish_slug):
#     public = Published.objects.get(slug=publish_slug)
#     if request.user.is_authenticated:
#         form = AddCommentForm()
#         if request.method == 'POST':
#             form = AddCommentForm(request.POST)
#             if form.is_valid():
#                 form.save()
#
#         context = {'menu': menu, 'title': 'Добавить комментарий', 'form': form}
#         return render(request, 'main/add_comment.html', context)
#     return HttpResponse('Необходимо войти в систему!')
