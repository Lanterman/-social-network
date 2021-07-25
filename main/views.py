from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView
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


def group_quit(request, group_slug):
    q = Groups.objects.get(slug=group_slug)
    q.users.remove(request.user)
    context = {'menu': menu, 'q': q, 'title': 'Выход выполнен успешно!'}
    return render(request, 'main/group_quit.html', context)


def group_enter(request, group_slug):
    q = Groups.objects.get(slug=group_slug)
    for user in Users.objects.all():
        if user.username == request.user.username:
            q.users.add(user)
    context = {'menu': menu, 'q': q, 'title': 'Вход выполнен успешно!'}
    return render(request, 'main/group_quit.html', context)


@login_required(login_url='/users/login/')
def detail_group(request, group_slug):
    group = Groups.objects.get(slug=group_slug)
    g = group.users.all()
    context = {'menu': menu, 'group': group, 'g': g, 'q': ''}
    for qi in g:
        if qi.username == request.user.username:
            context['q'] = qi.username
    return render(request, 'main/detail_group.html', context)


# class DetailGroup(DetailView):
#     template_name = 'main/detail_group.html'
#     slug_url_kwarg = 'group_slug'
#     model = Groups
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['menu'] = menu
#         return context


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


@login_required(login_url='/users/login/')
def add_comment_view(request, publish_slug):
    public = Published.objects.get(slug=publish_slug)
    form = AddCommentForm()
    if request.method == 'POST':
        form = AddCommentForm(request.POST)
        if form.is_valid():
            Comments.objects.create(biography=form.cleaned_data['biography'], published_id=public.id,
                                    users_id=request.user.pk)
            return redirect(public)
    context = {'menu': menu, 'title': 'Добавить комментарий', 'form': form}
    return render(request, 'main/add_comment.html', context)
