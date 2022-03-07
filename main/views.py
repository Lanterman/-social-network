from django.contrib.auth.decorators import login_required
from django.db.models import Q, Avg, Count, Prefetch
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView, CreateView, UpdateView
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin

from main import tasks
from main.form import *
from main.models import *
from main.utils import *
from users.form import MessageForm
from users.models import *


class NewsView(ListView):
    template_name = 'main/index.html'
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
        if request.user.is_authenticated:
            self.object = Groups.objects.exclude(users__username=request.user.username)[:3]
            self.group = Groups.objects.filter(users__username=request.user.username)
            self.published = Published.objects.filter(
                group_id__in=[gr.id for gr in self.group]).select_related('owner').annotate(
                rat=Avg('rating__star_id')).order_by('-date')
        else:
            self.object = Groups.objects.all()[:3]
            self.published = Published.objects.all().select_related('owner').annotate(
                rat=Avg('rating__star_id')).order_by('-date')
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return self.published


class HomeView(DataMixin, UpdateView):  # Оптимизировать
    model = Users
    form_class = AddPhotoForm
    template_name = 'main/home.html'
    pk_url_kwarg = 'user_pk'
    context_object_name = 'user'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Users.objects.all().prefetch_related('friends'))
        self.users = self.object.friends.all()
        self.group = Groups.objects.filter(users=self.object).prefetch_related('users')
        self.my_groups = Groups.objects.filter(owner_id=self.object.id).prefetch_related('users')
        self.stop = PostSubscribers.objects.filter(owner=self.object.username).select_related('user')
        self.user = ''
        if self.object.pk != request.user.pk:
            self.user = Users.objects.get(pk=request.user.pk)
            self.subs = PostSubscribers.objects.filter(
                Q(owner=self.user.username, user_id=self.object) |
                Q(owner=self.object.username, user_id=self.user)
            )
        else:
            self.subs = PostSubscribers.objects.filter(owner=self.object.username, escape=False).select_related('user')
        self.published = Published.objects.filter(owner_id=self.object.id).select_related('owner').annotate(
            rat=Avg('rating__star_id'))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        context['users'] = self.users
        context['groups'] = self.group
        context['users_init'] = 'друзей'
        context['center_friends'] = 'Друзья'
        context['page_obj'] = self.published
        context['primary'] = 'home'
        context['my_groups'] = self.my_groups
        context['owner'] = self.user
        context['subs'] = self.subs
        context['stop'] = self.stop
        return context | self.get_context()


class MessagesView(DataMixin, ListView):
    context_object_name = 'chats'
    template_name = 'main/messages.html'

    def get(self, request, *args, **kwargs):
        self.chats = Chat.objects.filter(members=request.user.id).prefetch_related(
            'members',
            Prefetch(
                'message_set',
                queryset=Message.objects.filter(chat__members=request.user.id),
                to_attr='set_mes'
            )
        )  # Отсортировать
        self.object = Groups.objects.exclude(users__username=request.user.username)[:3]
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.object
        context['title'] = 'Мои сообщения'
        context['act'] = 'search_messages'
        context['name'] = 'Поиск сообщений'
        return context | self.get_context()

    def get_queryset(self):
        return self.chats


class ChatDetailView(DataMixin, View):
    def get(self, request, chat_id):
        self.user = Users.objects.get(pk=request.user.pk)
        self.group = Groups.objects.exclude(users=self.user)[:3]
        self.chat = Chat.objects.prefetch_related('members').get(id=chat_id)
        messages = Message.objects.filter(chat_id=chat_id).select_related('author')
        if self.user in self.chat.members.all():
            messages.filter(is_readed=False).exclude(author_id=self.user.id).update(is_readed=True)
        else:
            self.chat = None
        context = {'chat': self.chat, 'form': MessageForm(), 'messages': messages, 'menu': menu,
                   'title': 'Мои сообщения', 'object': self.group}
        return render(request, 'main/chat.html', context)

    def post(self, request, chat_id):
        form = MessageForm(data=request.POST)
        if form.is_valid():
            Message.objects.create(**form.cleaned_data, chat_id=chat_id, author_id=request.user.pk)
            chat = Chat.objects.get(id=chat_id).members.all()
            if chat[0].pk == request.user.pk:
                user = chat[1]
            else:
                user = chat[0]
            user_name = user.get_full_name()
            if not user_name:
                user_name = user.username
            tasks.send_message.delay(user_name, user.email, chat_id)
        return redirect(reverse('chat', kwargs={'chat_id': chat_id}))


class CreateDialogView(View):
    def get(self, request, user_id):
        chats = Chat.objects.filter(members__in=[request.user.id, user_id]).annotate(c=Count('members')).filter(c=2)
        if chats.count():
            chat = chats.first()
        else:
            chat = Chat.objects.create()
            chat.members.add(request.user.pk)
            chat.members.add(user_id)
        return redirect(chat)


class FriendsView(DataMixin, SingleObjectMixin, ListView):
    template_name = 'main/friends.html'
    pk_url_kwarg = 'user_pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Мои друзья'
        context['act'] = 'search_friends'
        context['name'] = 'Поиск друзей'
        context['recommendation'] = 'друзья'
        context['object'] = self.object
        return context | self.get_context()

    def get(self, request, *args, **kwargs):
        self.users = Users.objects.filter(friends__pk=request.user.pk)
        self.object = Users.objects.exclude(friends=request.user.pk).exclude(pk=request.user.pk)[:3]
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return self.users


class GroupsView(DataMixin, ListView):
    template_name = 'main/groups.html'
    context_object_name = 'groups'

    def get(self, request, *args, **kwargs):
        self.group = Groups.objects.filter(users__pk=request.user.pk).prefetch_related('users')
        self.object = Groups.objects.exclude(users__pk=request.user.pk)[:3]
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Мои группы'
        context['object'] = self.object
        context['name'] = 'Поиск группы'
        context['act'] = 'search_group'
        return context | self.get_context()

    def get_queryset(self):
        return self.group


class AddGroup(DataMixin, CreateView):
    form_class = AddGroupForm
    template_name = 'main/add_pub_group.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создать группу'
        return context | self.get_context()

    def post(self, request, *args, **kwargs):
        form = AddGroupForm(request.POST, request.FILES)
        if form.is_valid():
            user = Users.objects.get(pk=request.user.pk)
            group = Groups.objects.create(**form.cleaned_data, owner_id=user.pk)
            tasks.send_message_about_group.delay(group.name, group.slug, user.email)
            return redirect(group)
        return super().post(request, *args, **kwargs)


class DetailGroupView(DataMixin, SingleObjectMixin, ListView):
    template_name = 'main/detail_group.html'
    paginate_by = 3
    slug_url_kwarg = 'group_slug'

    def get(self, request, *args, **kwargs):
        self.user = Users.objects.get(pk=request.user.pk)
        self.object = self.get_object(queryset=Groups.objects.all().prefetch_related('users').select_related('owner'))
        self.users = self.object.users.all()
        self.published = Published.objects.filter(group_id=self.object.id).select_related('owner').annotate(
            rat=Avg('rating__star_id')).order_by('-date')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['group'] = self.object
        context['user'] = self.object.owner
        context['users'] = self.users
        context['primary'] = 'home'
        context['user1'] = self.user
        return context | self.get_context()

    def get_queryset(self):
        return self.published


class AddPublished(DataMixin, CreateView):
    form_class = AddPublishedForm
    template_name = 'main/add_pub_group.html'
    slug_url_kwarg = 'group_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context | self.get_context(title='Создать запись')

    def post(self, request, *args, **kwargs):
        group = Groups.objects.get(slug=self.kwargs.get(self.slug_url_kwarg))
        form = AddPublishedForm(request.POST, request.FILES)
        if form.is_valid():
            user = Users.objects.get(pk=request.user.pk)
            published = Published.objects.create(**form.cleaned_data, group_id=group.pk, owner_id=user.pk)
            tasks.send_message_about_published.delay(published.name, published.slug, user.email)
            return redirect(group)
        return super().post(request, *args, **kwargs)


class DetailPublish(DetailView):
    model = Published
    slug_url_kwarg = 'publish_slug'
    template_name = 'main/detail_publish.html'
    queryset = Published.objects.all().select_related('group', 'owner').annotate(rat=Avg('rating__star_id'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['star_form'] = RatingForm()
        if self.request.user.is_authenticated:
            try:
                context['user1'] = Rating.objects.filter(published_id__name=self.object.name).select_related(
                    'star').get(
                    ip=self.request.user)
            except Exception:
                pass
        return context


class PublishedCommentsView(SingleObjectMixin, ListView):
    template_name = 'main/comments.html'
    paginate_by = 5
    slug_url_kwarg = 'publish_slug'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Published.objects.all())
        self.comments = Comments.objects.filter(published_id=self.object.id).select_related('users').prefetch_related(
            'like')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Комментарии'
        context['menu'] = menu
        context['published'] = self.object
        if self.request.user.is_authenticated:
            context['user1'] = Users.objects.get(username=self.request.user.username)
        return context

    def get_queryset(self):
        return self.comments


class AddCommentView(DataMixin, CreateView):
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
        return context | self.get_context(title='Добавить комментарий')


# Logic

def del_group(request, group_slug):
    Groups.objects.get(slug=group_slug).delete()
    return redirect(reverse('groups', kwargs={'user_pk': request.user.pk}))


def del_pub_group(request, pub_slug, group_slug):
    group = Groups.objects.get(slug=group_slug)
    Published.objects.get(slug=pub_slug).delete()
    return redirect(group)


def del_published(request, pub_slug):
    user = Users.objects.get(pk=request.user.pk)
    Published.objects.get(slug=pub_slug).delete()
    return redirect(user)


class AbstractUpdate(DataMixin, UpdateView):
    template_name = 'main/add_pub_group.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context | self.get_context(title='Редактирование', add='Ошибка изменения!')


class UpdateGroup(AbstractUpdate):
    model = Groups
    form_class = AddGroupForm
    slug_url_kwarg = 'group_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context | self.get_context(delete='No')


class UpdatePublished(AbstractUpdate):
    model = Published
    form_class = AddPublishedForm
    slug_url_kwarg = 'pub_slug'


def friend_activity(request, user_pk):
    q = Users.objects.get(pk=user_pk)
    user = Users.objects.get(pk=request.user.pk)
    try:
        subs = PostSubscribers.objects.select_related('user').get(
            Q(owner=user.username, user_id=q.pk) |
            Q(owner=q.username, user_id=user.pk)
        )
    except Exception:
        subs = ''
    if q in user.friends.all():
        q.friends.remove(request.user)
        PostSubscribers.objects.create(owner=user.username, user_id=q.id)
    elif not subs:
        PostSubscribers.objects.create(owner=q.username, user_id=user.id)
    elif subs.owner != q.username:
        user.friends.add(q)
        PostSubscribers.objects.filter(owner=user.username, user_id=q.id).delete()
    elif subs.owner == q.username:
        PostSubscribers.objects.filter(owner=q.username, user_id=user.id).delete()
    return redirect(q)


def friend_hide(request, user_pk):
    q = Users.objects.get(pk=user_pk)
    user = Users.objects.get(pk=request.user.pk)
    PostSubscribers.objects.filter(owner=user.username, user_id=q.id).update(escape=True)
    return redirect(user)


def friend_accept(request, user_pk):
    q = Users.objects.get(pk=user_pk)
    user = Users.objects.get(pk=request.user.pk)
    user.friends.add(q)
    PostSubscribers.objects.filter(owner=user.username, user_id=q.id).delete()
    return redirect(user)


def friend_del_primary(request, user_pk):
    q = Users.objects.get(pk=user_pk)
    user = Users.objects.get(pk=request.user.pk)
    user.friends.remove(q)
    PostSubscribers.objects.create(owner=user.username, user_id=q.id)
    return redirect(reverse('friends', kwargs={'user_pk': user.pk}))


def group_activity(request, group_slug):
    q = Groups.objects.prefetch_related('users').get(slug=group_slug)
    user = Users.objects.get(pk=request.user.pk)
    if user in q.users.all():
        q.users.remove(request.user)
    else:
        q.users.add(user)
    return redirect(q)


def group_quit_primary(request, group_slug):
    q = Groups.objects.get(slug=group_slug)
    q.users.remove(request.user)
    return redirect(reverse('groups', kwargs={'user_pk': request.user.pk}))


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
    comment = Comments.objects.prefetch_related('like').get(id=com_id)
    user = Users.objects.get(username=request.user.username)
    if user in comment.like.all():
        comment.like.remove(user)
    else:
        comment.like.add(user)
    return redirect(comment)


class SearchPublished(NewsView):
    def get_queryset(self):
        return Published.objects.filter(
            Q(name__icontains=self.request.GET.get('search')) |
            Q(owner__username__icontains=self.request.GET.get('search'))
        ).select_related('owner').annotate(rat=Avg('rating__star_id')).order_by('-date')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['empty'] = 'Нет записей соответствующих запросу!'
        context['search'] = f'search={self.request.GET.get("search")}&'
        return context


class SearchGroups(GroupsView):
    def get_queryset(self):
        return self.group.filter(name__icontains=self.request.GET.get('search'))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['empty'] = 'Нет групп соответствующих запросу!'
        context['global'] = Groups.objects.filter(name__icontains=self.request.GET.get('search')).prefetch_related(
            'users')
        return context


class SearchFriends(FriendsView):
    def get_queryset(self):
        queryset = self.users.filter(
            Q(username__icontains=self.request.GET.get('search')) |
            Q(first_name__icontains=self.request.GET.get('search')) |
            Q(last_name__icontains=self.request.GET.get('search'))
        )
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['empty'] = 'Нет пользователей соответствующих запросу!'
        context['global'] = Users.objects.filter(
            Q(username__icontains=self.request.GET.get('search')) |
            Q(first_name__icontains=self.request.GET.get('search')) |
            Q(last_name__icontains=self.request.GET.get('search'))
        ).exclude(pk=self.request.user.pk)
        return context


class SearchMessages(MessagesView):  # Убрать из members текущего пользователя(из запроса, а не базы данных)
    def get_queryset(self):
        return self.chats.filter(
            Q(members__first_name__icontains=self.request.GET.get('search')) |
            Q(members__last_name__icontains=self.request.GET.get('search'))
        ).distinct()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['empty'] = 'Нет диалогов соответствующих запросу!'
        return context
