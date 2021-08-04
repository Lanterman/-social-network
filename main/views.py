from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView, CreateView, UpdateView
from django.views.generic.detail import SingleObjectMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from main.form import *
from main.models import *
from main.serializers import UserPublishedSerializer

menu = [
    {'name': 'Главная страница', 'url': 'home'},
    {'name': 'Сообщения', 'url': 'messages'},
    {'name': 'Друзья', 'url': 'friends'},
    {'name': 'Группы', 'url': 'groups'}
]


def news(request):  # ?????????
    if request.user.is_authenticated:
        group = Groups.objects.exclude(users__username=request.user.username)[:5]
    else:
        group = Groups.objects.all()
    public = Published.objects.all().order_by('-date')
    paginator = Paginator(public, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'title': 'Новости', 'page_obj': page_obj, 'menu': menu, 'group': group}
    return render(request, 'main/index.html', context)


# class NewsView(ListView):
#     template_name = 'main/index.html'
#     model = Published
#     paginate_by = 5
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['menu'] = menu
#         context['title'] = 'Новости'
#         context['group'] = Groups.objects.all
#         return context


# @login_required(login_url='/users/login/')
# def home(request):
#     users = Users.objects.get(username=request.user.username)
#     form = AddPhotoForm()
#     if request.method == 'POST':
#         form = AddPhotoForm(request.FILES)
#         if form.is_valid():
#             users.photo = request.FILES['photo']
#             users.save()
#             return redirect('home')
#     context = {'title': 'Главная страница', 'menu': menu, 'users': users, 'form': form}
#     return render(request, 'main/home.html', context)


class HomeView(LoginRequiredMixin, UpdateView):
    login_url = '/users/login/'
    model = Users
    form_class = AddPhotoForm
    template_name = 'main/home.html'
    pk_url_kwarg = 'user_pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        context['menu'] = menu
        return context


def messages(request, user_pk):
    return HttpResponse('Мои сообщения')


def friends(request, user_pk):
    return HttpResponse('Список друзей')


@login_required(login_url='/users/login/')
def groups(request, user_pk):  # ?????????
    group1 = Groups.objects.filter(users__pk=user_pk)
    group = Groups.objects.exclude(users__pk=user_pk)[:5]
    context = {'title': 'Мои группы', 'menu': menu, 'group': group, 'group1': group1}
    return render(request, 'main/groups.html', context)


class AddGroup(LoginRequiredMixin, CreateView):
    login_url = '/users/login/'
    form_class = AddGroupForm
    template_name = 'main/add_group.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создать группу'
        context['menu'] = menu
        return context

    def form_valid(self, form):
        group = form.save()
        group.slug = group.name
        group.save()
        return redirect(group)


@login_required(login_url='/users/login/')
def group_quit(request, group_slug):
    q = Groups.objects.get(slug=group_slug)
    q.users.remove(request.user)
    context = {'menu': menu, 'q': q, 'title': 'Выход выполнен успешно!'}
    return render(request, 'main/group_quit.html', context)


@login_required(login_url='/users/login/')
def group_enter(request, group_slug):
    q = Groups.objects.get(slug=group_slug)
    for user in Users.objects.all():
        if user.username == request.user.username:
            q.users.add(user)
    context = {'menu': menu, 'q': q, 'title': 'Вход выполнен успешно!'}
    return render(request, 'main/group_quit.html', context)


def detail_group(request, group_slug):  # ?????????
    group = Groups.objects.get(slug=group_slug)
    g = group.users.all()
    group1 = group.published_set.all().order_by('-date')
    paginator = Paginator(group1, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'menu': menu, 'group': group, 'g': g, 'q': '', 'page_obj': page_obj}
    for qi in g:
        if qi.username == request.user.username:
            context['q'] = qi.username
    return render(request, 'main/detail_group.html', context)


# class DetailGroup(LoginRequiredMixin, SingleObjectMixin, ListView):
#     login_url = '/users/login/'
#     template_name = 'main/detail_group.html'
#     paginate_by = 3
#     slug_url_kwarg = 'group_slug'
#
#     def get(self, request, *args, **kwargs):
#         self.object = self.get_object(queryset=Groups.objects.all())
#         return super().get(request, *args, **kwargs)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['menu'] = menu
#         context['group'] = self.object
#         return context
#
#     def get_queryset(self):
#         return self.object.users.all().select_related('group')


@login_required(login_url='/users/login/')
def add_published(request, group_slug):
    form = AddPublishedForm()
    group = Groups.objects.get(slug=group_slug)
    if request.method == 'POST':
        form = AddPublishedForm(request.POST, request.FILES)
        if form.is_valid():
            Published.objects.create(**form.cleaned_data, group_id=group.pk)
            return redirect(group)
    context = {'menu': menu, 'title': 'Добавить запись', 'form': form}
    return render(request, 'main/add_published.html', context)


class DetailPublish(DetailView):
    model = Published
    slug_url_kwarg = 'publish_slug'
    template_name = 'main/detail_publish.html'
    queryset = Published.objects.all().select_related('group')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['star_form'] = RatingForm()
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
            Comments.objects.create(**form.cleaned_data, published_id=public.id, users_id=request.user.pk)
            return redirect(public)
    context = {'menu': menu, 'title': 'Добавить комментарий', 'form': form}
    return render(request, 'main/add_comment.html', context)


class UserPublishedRelationView(UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserPublishedRelation.objects.all()
    serializer_class = UserPublishedSerializer
    lookup_field = 'published'

    def get_object(self):
        obj, _ = UserPublishedRelation.objects.get_or_create(user=self.request.user,
                                                             published_id=self.kwargs['published'])
        return obj
