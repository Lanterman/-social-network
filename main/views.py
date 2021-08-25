from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
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
        context['object'] = self.object
        context['name'] = 'Поиск записи'
        context['act'] = 'search_published'
        return context

    def get(self, request, *args, **kwargs):
        self.public = []
        published = Published.objects.all().select_related('owner', 'group')
        if request.user.is_authenticated:
            self.object = Groups.objects.exclude(users__username=request.user.username)[:3]
            self.group1 = Groups.objects.filter(users__username=request.user.username)
            for p in published:
                if p.group in self.group1:
                    self.public += [[p, p.average(p.name)]]  # Оптимизировать вывод среднего значения рейтинга
        else:
            self.object = Groups.objects.all()[:3]
            for p in published:
                self.public += [[p, p.average(p.name)]]  # Оптимизировать вывод среднего значения рейтинга
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return self.public


class HomeView(LoginRequiredMixin, UpdateView):  # Добавлять в друзья только с согласием юзера и вывод групп
    login_url = '/users/login/'
    model = Users
    form_class = AddPhotoForm
    template_name = 'main/home.html'
    pk_url_kwarg = 'user_pk'
    context_object_name = 'user'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Users.objects.all())
        self.users = self.object.friends.all()
        self.user = ''
        if self.object.pk != request.user.pk:
            self.user = Users.objects.get(pk=request.user.pk)
        published = Published.objects.filter(owner=self.object).select_related('owner')
        self.public = []
        for p in published:
                self.public += [[p, p.average(p.name)]]  # Оптимизировать вывод среднего значения рейтинга
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        context['menu'] = menu
        context['users'] = self.users
        context['users_init'] = 'друзей'
        context['center_friends'] = 'Друзья'
        context['page_obj'] = self.public
        if self.user in self.users:
            context['yes'] = 'Yes'
        return context


def messages(request, user_pk):
    return HttpResponse('Мои сообщения')


class FriendsView(LoginRequiredMixin, SingleObjectMixin, ListView):
    Model = Users
    login_url = 'users/login'
    template_name = 'main/friends.html'
    pk_url_kwarg = 'user_pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Мои друзья'
        context['empty'] = 'У вас нет друзей!'
        context['act'] = 'search_friends'
        context['object'] = self.object
        context['name'] = 'Поиск друзей'
        context['recommendation'] = 'друзья'
        return context

    def get(self, request, *args, **kwargs):
        self.users = Users.objects.filter(friends__pk=request.user.pk)
        self.object = Users.objects.exclude(friends=request.user.pk).exclude(pk=request.user.pk)[:3]
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return self.users


class GroupsView(LoginRequiredMixin, ListView):
    login_url = '/users/login/'
    template_name = 'main/groups.html'
    model = Groups
    context_object_name = 'groups'

    def get(self, request, *args, **kwargs):
        self.group1 = Groups.objects.filter(users__pk=request.user.pk).prefetch_related('users')
        self.object = Groups.objects.exclude(users__pk=request.user.pk)[:3]
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Мои группы'
        context['object'] = self.object
        context['name'] = 'Поиск группы'
        context['act'] = 'search_group'
        return context

    def get_queryset(self):
        return self.group1


class AddGroup(LoginRequiredMixin, CreateView):
    login_url = '/users/login/'
    form_class = AddGroupForm
    template_name = 'main/add_pub_group.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создать группу'
        context['menu'] = menu
        context['add'] = 'Ошибка создания группы!'
        return context


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
        if self.user1 in self.users:
            context['subscriber'] = 'Yes'
        return context

    def get_queryset(self):
        return self.published


class AddPublished(LoginRequiredMixin, CreateView):
    login_url = '/users/login/'
    form_class = AddPublishedForm
    template_name = 'main/add_pub_group.html'
    slug_url_kwarg = 'group_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создать запись'
        context['menu'] = menu
        context['add'] = 'Ошибка создания записи!'
        return context

    def post(self, request, *args, **kwargs):
        group = Groups.objects.get(slug=self.kwargs.get(self.slug_url_kwarg))
        form = AddPublishedForm(request.POST, request.FILES)
        if form.is_valid():
            Published.objects.create(**form.cleaned_data, group_id=group.pk, owner_id=request.user.pk)
            return redirect('news')
        return super().post(request, *args, **kwargs)


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
            self.user1 = request.user
        return super().get(request, *args, **kwargs)


class PublishedCommentsView(SingleObjectMixin, ListView):
    template_name = 'main/comments.html'
    paginate_by = 5
    slug_url_kwarg = 'publish_slug'

    def get(self, request, *args, **kwargs):
        self.user = ''
        if request.user.is_authenticated:
            self.user = Users.objects.get(username=request.user.username)
        self.object = self.get_object(queryset=Published.objects.all())
        self.comments = Comments.objects.filter(published=self.object).select_related('users').prefetch_related('like')  # Жадный запрос
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
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Добавить комментарий'
        return context


# Logic

def friend_del_primary(request, user_pk):
    q = Users.objects.get(pk=user_pk)
    q.friends.remove(request.user)
    return redirect(q)


def friend_add_primary(request, user_pk):
    q = Users.objects.get(pk=user_pk)
    user = Users.objects.get(pk=request.user.pk)
    user.friends.add(q)
    return redirect(q)


def friend_del(request, friend_pk):
    q = Users.objects.get(pk=friend_pk)
    user = Users.objects.get(pk=request.user.pk)
    user.friends.remove(q)
    return redirect(reverse('friends', kwargs={'user_pk': user.pk}))


def group_quit(request, group_slug):
    q = Groups.objects.get(slug=group_slug)
    q.users.remove(request.user)
    return redirect(q)


def group_quit_primary(request, group_slug):
    q = Groups.objects.get(slug=group_slug)
    user = Users.objects.get(pk=request.user.pk)
    q.users.remove(request.user)
    return redirect(reverse('groups', kwargs={'user_pk': user.pk}))


def group_enter(request, group_slug):
    q = Groups.objects.get(slug=group_slug)
    user = Users.objects.get(pk=request.user.pk)
    q.users.add(user)
    return redirect(q)


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


class SearchPublished(NewsView):  # Оптимизировать дубли и рейтинг
    def get(self, request, *args, **kwargs):
        self.published = []
        self.public = Published.objects.filter(
            Q(name__icontains=self.request.GET.get('search')) |
            Q(owner__username__icontains=self.request.GET.get('search'))
        )  # Только из вступивших групп
        for p in self.public:
            self.published += [[p, p.average(p.name)]]
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return self.published

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['empty'] = 'Нет записей соответствующих запросу'
        context['search'] = f'search={self.request.GET.get("search")}&'
        return context


class SearchGroups(GroupsView):
    def get_queryset(self):
        return Groups.objects.filter(name__icontains=self.request.GET.get('search'))  # Только вступившие группы

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['empty'] = 'Нет групп соответствующих запросу'
        return context


class SearchFriends(FriendsView):
    def get_queryset(self):  # Выводить только друзей соответствующих запросу(сейчас проверяет всех пользователей)
        queryset = Users.objects.filter(
            Q(username__icontains=self.request.GET.get('search')) |
            Q(first_name__icontains=self.request.GET.get('search')) |
            Q(last_name__icontains=self.request.GET.get('search'))
        )
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['empty'] = 'Нет друзей соответствующих запросу'
        return context
