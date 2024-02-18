from django.core.exceptions import PermissionDenied
from django.db.models import Q, Avg, Count, Prefetch
from django.db.models.base import Model as Model
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import DetailView, ListView, CreateView, UpdateView
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin

from src.main import tasks
from src.main.form import AddGroupForm, AddPhotoForm, AddPublishedForm, RatingForm
from src.main.models import Comment, Publication, Group, Rating
from src.main.utils import *
from src.users.models import User, Follower, Chat, Message


class NewsView(ListView): ### Search groups with ws
    """News page endpoint"""

    template_name = 'main/index.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Новости'
        context['object'] = self.object
        context['name'] = 'Search for publications'
        context['act'] = 'search_published'
        return context

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            self.object = Group.objects.exclude(followers__pk=request.user.pk).exclude(owner__pk=request.user.pk)[:4]
            self.group = Group.objects.filter(followers__username=request.user.username)
            self.publications = Publication.objects.filter(
                group_id__in=[gr.id for gr in self.group]).select_related('owner').annotate(
                rat=Avg('rating__star_id')).order_by('-date')            
        else:
            self.object = Group.objects.all()[:4]
            self.publications = Publication.objects.all().select_related('owner').annotate(
                rat=Avg('rating__star_id')).order_by('-date')
        
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return self.publications


class HomeView(DataMixin, UpdateView): # Проверить оптимизацию эндпоинта. Продолжить модернизацию вспомогательных функций
    """User page"""

    model = User
    form_class = AddPhotoForm
    template_name = 'main/home.html'
    pk_url_kwarg = 'user_pk'
    context_object_name = 'user'

    @staticmethod
    def check_if_i_am_follower(followers, user_id: int) -> bool | None:
        """Checking if i'm a follower"""

        for follower in followers:
            if follower.follower_id.id == user_id:
                return True
    
    @staticmethod
    def check_if_i_am_sub(subs, user_id: int) -> bool | None:
        """Checking if i'm a sub"""

        for sub in subs:
            if sub.subscription_id.id == user_id:
                return True

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=User.objects.all().prefetch_related(
            'followers__follower_id', 'subscriptions__subscription_id', 'groups_followers', 'my_groups')
        )

        self.followers = self.object.followers.all()
        self.subs = self.object.subscriptions.all()
        self.groups = self.object.groups_followers.all()
        self.my_groups = self.object.my_groups.all()

        self.new_followers = [follower for follower in self.followers if not follower.is_checked]
        self.old_followers = [follower for follower in self.followers if follower.is_checked]

        self.publications = Publication.objects.filter(owner_id=self.object.id).select_related('owner').annotate(
            rat=Avg('rating__star_id'))

        return self.render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groups'] = self.groups
        context['my_groups'] = self.my_groups
        context['page_obj'] = self.publications
        context['subs'] = self.subs
        context['followers'] = self.old_followers
        context["new_followers"] = self.new_followers
        context["count_old_followers"] = len(self.old_followers)
        context["count_new_followers"] = len(self.new_followers)
        
        if self.object.id != self.request.user.id:
            context["i_am_follower"] = self.check_if_i_am_follower(self.followers, self.request.user.id)
            context["i_am_sub"] = self.check_if_i_am_sub(self.subs, self.request.user.id)

        return context | self.get_context()


class MessagesView(DataMixin, ListView):
    """User messages page"""

    context_object_name = 'chats'
    template_name = 'main/messages.html'

    def get(self, request, *args, **kwargs):
        message = Message.objects.filter(chat_id__members=request.user.id).select_related('author_id')

        self.chats = Chat.objects.filter(members=request.user.id).prefetch_related(
            'members',
            Prefetch('message_set', queryset= message, to_attr='set_mes')
        ).annotate(count_mes=Count("message_set")).filter(count_mes__gt=0)

        self.object = Group.objects.exclude(followers__pk=request.user.pk).exclude(owner__pk=request.user.pk)[:4]
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.object
        context['title'] = 'My messages'
        context['act'] = 'search_messages'
        context['name'] = 'Search messages'
        return context | self.get_context()

    def get_queryset(self):
        return sorted(self.chats, key=lambda x: x.set_mes[0].pub_date, reverse=True)


class ChatDetailView(DataMixin, View):
    """Chat page"""

    def get(self, request, chat_id):
        self.groups = Group.objects.exclude(followers__pk=request.user.pk).exclude(owner__pk=request.user.pk)[:4]
        self.chat = Chat.objects.prefetch_related('members').get(id=chat_id)

        if request.user not in self.chat.members.all():
            raise PermissionDenied()
        
        messages = Message.objects.filter(chat_id=chat_id).select_related('author_id').order_by("pub_date")
        messages.filter(is_readed=False).exclude(author_id__id=request.user.id).update(is_readed=True)

        context = {'chat': self.chat, 'messages': messages, 'menu': menu, 'title': 'My message',
                   'object': self.groups, "chat_id": chat_id}
        return render(request, 'main/chat.html', context)

    @staticmethod
    def post(request, chat_id):
        message = request.POST.get("message")
        Message.objects.create(message=message, chat_id_id=chat_id, author_id_id=request.user.pk)
        Message.objects.filter(chat_id_id=chat_id, is_readed=False).exclude(author_id_id=request.user.id).update(is_readed=True)
        return HttpResponse(status=200)


class CreateDialogView(View):
    """Page for creating new chat"""

    @staticmethod
    def get(request, user_id):
        chats = Chat.objects.filter(members__in=[request.user.id, user_id]).annotate(c=Count('members')).filter(c=2)
        if chats.count():
            chat = chats.first()
        else:
            chat = Chat.objects.create()
            chat.members.add(request.user.pk)
            chat.members.add(user_id)
        return redirect(chat)


class FollowersView(DataMixin, SingleObjectMixin, ListView):
    """User friends page"""

    template_name = 'main/my_users.html'
    pk_url_kwarg = 'user_pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'My followers'
        context['act'] = 'search_followers'
        context['name'] = 'Search followers'
        context['object'] = self.object
        return context | self.get_context()

    def get(self, request, *args, **kwargs):
        self.qs_main_followers = Follower.objects.filter(subscription_id__id=request.user.id).select_related("follower_id")

        self.followers = [follower.follower_id for follower in self.qs_main_followers]
        self.users_id = [user.id for user in self.followers]

        self.object = User.objects.exclude(id__in=self.users_id).exclude(id=request.user.id)[:4]

        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return self.followers


class SubscriptionsView(DataMixin, SingleObjectMixin, ListView):
    """User friends page"""

    template_name = 'main/my_users.html'
    pk_url_kwarg = 'user_pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'My subccriptions'
        context['act'] = 'search_subscriptions'
        context['name'] = 'Search subccriptions'
        context['object'] = self.object
        return context | self.get_context()

    def get(self, request, *args, **kwargs):
        self.qs_main_subs = Follower.objects.filter(follower_id=request.user.id).select_related("subscription_id")

        self.subs = [sub.subscription_id for sub in self.qs_main_subs]
        self.users_id = [user.id for user in self.subs]

        self.object = User.objects.exclude(id__in=self.users_id).exclude(id=request.user.id)[:4]

        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return self.subs


class GroupsView(DataMixin, ListView): ### Search groups with ws
    """User groups page"""

    template_name = 'main/groups.html'
    context_object_name = 'groups'

    def get(self, request, *args, **kwargs):
        self.group = Group.objects.filter(
            Q(followers__pk=request.user.pk) | Q(owner__pk=request.user.pk)
        ).prefetch_related('followers').distinct()

        self.object = Group.objects.exclude(followers__pk=request.user.pk).exclude(owner__pk=request.user.pk)[:4]
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'My groups'
        context['object'] = self.object
        context['name'] = 'Search for groups'
        context['act'] = 'search_group'
        return context | self.get_context()

    def get_queryset(self):
        return self.group


class AddGroup(DataMixin, CreateView):
    """Page for creating new group"""

    form_class = AddGroupForm
    template_name = 'main/add_pub_group.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create group'
        return context | self.get_context()

    def post(self, request, *args, **kwargs):
        form = AddGroupForm(request.POST, request.FILES)
        if form.is_valid():
            group = Group.objects.create(**form.cleaned_data, owner_id=request.user.pk)
            # tasks.send_message_about_group.delay(group.name, group.slug, user.email)
            group.slug = group.name.replace(" ", "_")
            group.save()
            return redirect(group)
        return super().post(request, *args, **kwargs)


class DetailGroupView(DataMixin, SingleObjectMixin, ListView):
    """Detail group page"""

    template_name = 'main/detail_group.html'
    paginate_by = 3
    slug_url_kwarg = 'group_slug'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Group.objects.all().prefetch_related('followers').select_related('owner'))
        self.followers = self.object.followers.all()
        self.published = Publication.objects.filter(group_id=self.object.id).select_related('owner').annotate(
            rat=Avg('rating__star_id')).order_by('-date')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['group'] = self.object
        context['followers'] = self.followers
        return context | self.get_context()

    def get_queryset(self):
        return self.published


class AddPublished(DataMixin, CreateView):
    """PAge for creating new publish"""

    form_class = AddPublishedForm
    template_name = 'main/add_pub_group.html'
    slug_url_kwarg = 'group_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context | self.get_context(title='Create publication')

    def post(self, request, *args, **kwargs):
        group = Group.objects.get(slug=self.kwargs.get(self.slug_url_kwarg))
        form = AddPublishedForm(request.POST, request.FILES)
        if form.is_valid():
            published = Publication.objects.create(**form.cleaned_data, group_id=group.pk, owner_id=request.user.pk)
            published.slug = published.name.replace(" ", "_")
            published.save()
            # tasks.send_message_about_published.delay(published.name, published.slug, user.email)
            return redirect(group)
        return super().post(request, *args, **kwargs)


class DetailPublication(DataMixin, DetailView):
    """Detail publish page"""

    model = Publication
    slug_url_kwarg = 'publish_slug'
    template_name = 'main/detail_publish.html'
    queryset = Publication.objects.all().select_related('group', 'owner').annotate(rat=Avg('rating__star_id'))
    context_object_name = "publication"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['star_form'] = RatingForm()

        if self.request.user.is_authenticated:
            try:
                context['rating'] = Rating.objects.filter(publication_id__name=self.object.name).select_related(
                    'star').get(
                    ip=self.request.user.username)
            except Exception:
                pass

        return context | self.get_context()


class PublishedCommentsView(SingleObjectMixin, ListView):
    """Publication comments page"""

    template_name = 'main/comments.html'
    slug_url_kwarg = 'publish_slug'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Publication.objects.all())
        self.comments = Comment.objects.filter(publication_id=self.object.id).select_related('users').prefetch_related(
            'like')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Комментарии'
        context['menu'] = menu
        context['publication'] = self.object
        return context

    def get_queryset(self):
        return self.comments


# Logic

def del_group(request, group_slug):
    """Delete group"""

    Group.objects.get(slug=group_slug).delete()
    return redirect(reverse('groups', kwargs={'user_pk': request.user.pk}))


def del_pub_group(request, pub_slug, group_slug):
    """Delete group for owner"""

    group = Group.objects.get(slug=group_slug)
    Publication.objects.get(slug=pub_slug).delete()
    return redirect(group)


def del_published(request, pub_slug):
    """Delete published for owner group or owner publication"""

    Publication.objects.get(slug=pub_slug).delete()
    return redirect(request.user)


class AbstractUpdate(DataMixin, UpdateView):
    template_name = 'main/add_pub_group.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context | self.get_context(title='Change', add='Error!')


class UpdateGroup(AbstractUpdate):
    model = Group
    form_class = AddGroupForm
    slug_url_kwarg = 'group_slug'

    def form_valid(self, form):
        group = form.save()
        group.slug = group.name.replace(" ", "")
        group.save()
        return redirect(group)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context | self.get_context(delete='No')


class UpdatePublished(AbstractUpdate):
    model = Publication
    form_class = AddPublishedForm
    slug_url_kwarg = 'pub_slug'

    def form_valid(self, form):
        publish = form.save()
        publish.slug = publish.name.replace(" ", "")
        publish.save()
        return redirect(publish)


def friend_hide(request, user_pk): ###
    """Leave in subscribers"""

    q = User.objects.get(pk=user_pk)
    Follower.objects.filter(owner=request.user.username, user_id=q.id).update(escape=True)
    return redirect(request.user)


def friend_del_primary(request, user_pk): ###
    """Delete from friends"""

    q = User.objects.get(pk=user_pk)
    request.user.friends.remove(q)
    Follower.objects.create(owner=request.user.username, user_id=q.id)
    return redirect(reverse('friends', kwargs={'user_pk': request.user.pk}))


def group_activity(request, group_slug):
    """logic for group entry"""

    q = Group.objects.prefetch_related('followers').get(slug=group_slug)
    if request.user in q.followers.all():
        q.followers.remove(request.user)
    else:
        q.followers.add(request.user)
    return redirect(q)


def group_quit_primary(request, group_slug):
    """Leave group"""

    q = Group.objects.get(slug=group_slug)
    q.followers.remove(request.user)
    return redirect(reverse('groups', kwargs={'user_pk': request.user.pk}))


class AddStarRating(View):
    """Set star rating"""

    @staticmethod
    def post(request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=request.user.username,
                publication_id_id=int(request.POST.get("publication")),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)


class SearchPublished(NewsView): ### ws
    """Search for publications by name or owner username"""

    def get_queryset(self):
        return Publication.objects.filter(
            Q(name__icontains=self.request.GET.get('search')) |
            Q(owner__username__icontains=self.request.GET.get('search'))
        ).select_related('owner').annotate(rat=Avg('rating__star_id')).order_by('-date')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['empty'] = 'Нет записей соответствующих запросу!'
        context['search'] = f'search={self.request.GET.get("search")}&'
        return context


class SearchGroups(GroupsView): ### ws
    """Search for groups by name"""

    def get_queryset(self):
        return self.group.filter(name__icontains=self.request.GET.get('search'))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['empty'] = 'Нет групп соответствующих запросу!'
        context['global'] = Group.objects.filter(name__icontains=self.request.GET.get('search')).prefetch_related(
            'users')
        return context


class SearchFollowers(FollowersView): ### ws
    """Search for followers by username, first name or last name"""

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
        context['global'] = User.objects.filter(
            Q(username__icontains=self.request.GET.get('search')) |
            Q(first_name__icontains=self.request.GET.get('search')) |
            Q(last_name__icontains=self.request.GET.get('search'))
        ).exclude(pk=self.request.user.pk)
        return context


class SearchSubscriptions(SubscriptionsView): ### ws
    """Search for subscriptions by username, first name or last name"""

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
        context['global'] = User.objects.filter(
            Q(username__icontains=self.request.GET.get('search')) |
            Q(first_name__icontains=self.request.GET.get('search')) |
            Q(last_name__icontains=self.request.GET.get('search'))
        ).exclude(pk=self.request.user.pk)
        return context


class SearchMessages(MessagesView):  # Убрать из members текущего пользователя(из запроса, а не базы данных) ### ws
    """Search for messages by last name or first name of members"""

    def get_queryset(self):
        return self.chats.filter(
            Q(members__first_name__icontains=self.request.GET.get('search')) |
            Q(members__last_name__icontains=self.request.GET.get('search'))
        ).distinct()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['empty'] = 'Нет диалогов соответствующих запросу!'
        return context
