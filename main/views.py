from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import DetailView, ListView, CreateView, UpdateView
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin

from main.form import *
from main.models import *

menu = [
    {'name': 'Главная страница', 'url': 'home'},
    {'name': 'Сообщения', 'url': 'messages'},
    {'name': 'Друзья', 'url': 'friends'},
    {'name': 'Группы', 'url': 'groups'}
]


class NewsView(ListView):
    template_name = 'main/index.html'
    model = Published
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Новости'
        context['group'] = self.group
        context['empty'] = 'Новости отсутствуют'
        return context

    def get(self, request, *args, **kwargs):
        self.public = []
        if request.user.is_authenticated:
            self.group = Groups.objects.exclude(users__username=request.user.username)[:5]
            self.group1 = Groups.objects.filter(users__username=request.user.username)
            for public in self.group1:
                for p in public.published_set.all().select_related('owner'):
                    self.public += [[p, p.average(p.name)]]  # Оптимизировать вывод среднего значения рейтинга
        else:
            self.group = Groups.objects.all()[:5]
            for p in Published.objects.all().select_related('owner'):
                self.public += [[p, p.average(p.name)]]  # Оптимизировать вывод среднего значения рейтинга
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return self.public  # Сделать чтоб записи шли вне зависимости от группы по дате


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


# @login_required(login_url='/users/login/')
# def groups(request, user_pk):  # ?????????
#     group1 = Groups.objects.filter(users__pk=user_pk)
#     group = Groups.objects.exclude(users__pk=user_pk)[:5]
#     context = {'title': 'Мои группы', 'menu': menu, 'group': group, 'group1': group1}
#     return render(request, 'main/groups.html', context)


class GroupsView(LoginRequiredMixin, DetailView):
    login_url = '/users/login/'
    template_name = 'main/groups.html'
    pk_url_kwarg = 'user_pk'
    model = Users

    def get(self, request, *args, **kwargs):
        self.group1 = Groups.objects.filter(users__pk=request.user.pk)
        self.group = Groups.objects.exclude(users__pk=request.user.pk)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Мои группы'
        context['group1'] = self.group1
        context['group'] = self.group
        return context


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


def group_quit(request, group_slug):
    q = Groups.objects.get(slug=group_slug)
    q.users.remove(request.user)
    return redirect(q)


def group_enter(request, group_slug):
    q = Groups.objects.get(slug=group_slug)
    for user in Users.objects.all():
        if user.username == request.user.username:
            q.users.add(user)
    return redirect(q)


# def detail_group(request, group_slug):  # ?????????
#     group = Groups.objects.get(slug=group_slug)
#     g = group.users.all()
#     group1 = group.published_set.all().order_by('-date')
#     paginator = Paginator(group1, 3)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     context = {'menu': menu, 'group': group, 'g': g, 'q': '', 'page_obj': page_obj}
#     for qi in g:
#         if qi.username == request.user.username:
#             context['q'] = qi.username
#     return render(request, 'main/detail_group.html', context)


class DetailGroupView(LoginRequiredMixin, SingleObjectMixin, ListView):
    login_url = '/users/login/'
    template_name = 'main/detail_group.html'
    paginate_by = 3
    slug_url_kwarg = 'group_slug'

    def get(self, request, *args, **kwargs):
        self.user1 = Users.objects.get(pk=request.user.pk)
        self.object = self.get_object(queryset=Groups.objects.all())
        self.users = self.object.users.all()
        self.published = []
        for p in self.object.published_set.all().select_related('owner'):
            self.published += [[p, p.average(p.name)]]  # Оптимизировать вывод среднего значения рейтинга
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['group'] = self.object
        context['users'] = self.users
        context['empty'] = 'Записи отсутствуют'
        if self.user1 in self.users:
            context['subscriber'] = 'Yes'
        return context

    def get_queryset(self):
        return self.published


# @login_required(login_url='/users/login/')
# def add_published(request, group_slug):
#     form = AddPublishedForm()
#     group = Groups.objects.get(slug=group_slug)
#     if request.method == 'POST':
#         form = AddPublishedForm(request.POST, request.FILES)
#         if form.is_valid():
#             Published.objects.create(**form.cleaned_data, group_id=group.pk, owner_id=request.user.pk)
#             return redirect(group)
#     context = {'menu': menu, 'title': 'Добавить запись', 'form': form}
#     return render(request, 'main/add_published.html', context)


class AddPublished(LoginRequiredMixin, CreateView):
    login_url = '/users/login/'
    form_class = AddPublishedForm
    template_name = 'main/add_published.html'
    slug_url_kwarg = 'group_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создать группу'
        context['menu'] = menu
        return context

    def post(self, request, *args, **kwargs):
        group = Groups.objects.get(slug=self.kwargs.get(self.slug_url_kwarg))
        form = AddPublishedForm(request.POST, request.FILES)
        if form.is_valid():
            Published.objects.create(**form.cleaned_data, group_id=group.pk, owner_id=request.user.pk)
        return redirect(group)


class DetailPublish(DetailView):  # Оптимизировать рейтинг
    model = Published
    slug_url_kwarg = 'publish_slug'
    template_name = 'main/detail_publish.html'
    queryset = Published.objects.all().select_related('group', 'owner')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['star_form'] = RatingForm()
        if self.user1:
            try:
                context['user1'] = Rating.objects.filter(published_id__name=self.object).select_related().get(ip=self.user1)
            except Exception:
                pass
        context['average'] = self.object.average(self.object)
        return context

    def get(self, request, *args, **kwargs):
        self.user1 = ''
        self.object = self.get_object(queryset=Published.objects.all())
        if request.user.is_authenticated:
            self.user1 = request.user.username
        return super().get(request, *args, **kwargs)


class PublishedCommentsView(SingleObjectMixin, ListView):
    template_name = 'main/comments.html'
    paginate_by = 3
    slug_url_kwarg = 'publish_slug'

    def get(self, request, *args, **kwargs):
        self.user = ''
        if request.user.is_authenticated:
            self.user = Users.objects.get(username=request.user.username)
        self.object = self.get_object(queryset=Published.objects.all())
        self.comments = Comments.objects.filter(published=self.object).select_related('users')  # Жадный запрос
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['published'] = self.object
        context['title'] = 'Комментарии'
        context['user1'] = self.user
        return context

    def get_queryset(self):
        return self.comments


# @login_required(login_url='/users/login/')
# def add_comment_view(request, publish_slug):
#     public = Published.objects.get(slug=publish_slug)
#     form = AddCommentForm()
#     if request.method == 'POST':
#         form = AddCommentForm(request.POST)
#         if form.is_valid():
#             Comments.objects.create(**form.cleaned_data, published_id=public.id, users_id=request.user.pk)
#             return redirect(public)
#     context = {'menu': menu, 'title': 'Добавить комментарий', 'form': form}
#     return render(request, 'main/add_comment.html', context)


class AddCommentView(LoginRequiredMixin, CreateView):
    login_url = '/users/login/'
    template_name = 'main/add_comment.html'
    slug_url_kwarg = 'publish_slug'
    form_class = AddCommentForm

    def post(self, request, *args, **kwargs):
        published = Published.objects.get(slug=self.kwargs.get(self.slug_url_kwarg))
        form = AddCommentForm(request.POST)
        if form.is_valid():
            comment = Comments.objects.create(**form.cleaned_data, published_id=published.id, users_id=request.user.pk)
            return redirect(comment)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Добавить комментарий'
        return context


class AddStarRating(View):
    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            self.user = Users.objects.get(username=request.user.username)
            Rating.objects.update_or_create(
                ip=self.user,
                published_id=int(request.POST.get("published")),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)


@login_required(login_url='/users/login/')
def like_view(request, com_id):
    comment = Comments.objects.get(id=com_id)
    user = Users.objects.get(username=request.user.username)
    if user in comment.like.all():
        comment.like.remove(user)
    else:
        comment.like.add(user)
    return redirect(comment)
