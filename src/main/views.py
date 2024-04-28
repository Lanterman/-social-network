from django.core.exceptions import PermissionDenied
from django.db.models import Q, Avg, Count, Prefetch
from django.db.models.base import Model as Model
from django.forms import BaseModelForm
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


class NewsView(ListView):
    """News page endpoint"""

    template_name = 'main/index.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'News'
        context['object'] = self.object
        context['name'] = 'Search for publications'
        return context

    def get(self, request, *args, **kwargs):
        # if a user is authenticated
        if request.user.is_authenticated:
            # recommended groups
            self.object = Group.objects.exclude(followers__pk=request.user.pk).exclude(owner__pk=request.user.pk)[:4]

            # publications of groups I follow
            self.group = Group.objects.filter(followers__username=request.user.username)
            self.publications = Publication.objects.filter(
                group_id__in=[gr.id for gr in self.group]).select_related('owner').annotate(
                rat=Avg('rating__star_id')).order_by('-date')

        # if a user isn't authenticated       
        else:
            # recommended groups
            self.object = Group.objects.all()[:4]

            # all publications
            self.publications = Publication.objects.all().select_related('owner').annotate(
                rat=Avg('rating__star_id')).order_by('-date')
        
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return self.publications


class HomeView(DataMixin, UpdateView):
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
        context['name'] = 'Search followers'
        context['object'] = self.object
        return context | self.get_context()

    def get(self, request, *args, **kwargs):
        # create a list of my followers
        self.qs_main_followers = Follower.objects.filter(subscription_id__id=request.user.id).select_related("follower_id")
        self.followers = [follower.follower_id for follower in self.qs_main_followers]

        # create a QuerySet of recommended users
        self.qs_main_subs = Follower.objects.filter(follower_id=request.user.id).select_related("subscription_id")
        self.users_id = [user.subscription_id.id for user in self.qs_main_subs]
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
        context['title'] = 'My subscriptions'
        context['name'] = 'Search users'
        context['object'] = self.object
        return context | self.get_context()

    def get(self, request, *args, **kwargs):
        # create a list of my subscriptions
        self.qs_main_subs = Follower.objects.filter(follower_id=request.user.id).select_related("subscription_id")
        self.subs = [sub.subscription_id for sub in self.qs_main_subs]

        # create a QuerySet of recommended users
        self.users_id = [user.id for user in self.subs]
        self.object = User.objects.exclude(id__in=self.users_id).exclude(id=request.user.id)[:4]

        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return self.subs


class GroupsView(DataMixin, ListView):
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
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        group = form.save(commit=False)
        group.slug = group.name.replace(" ", "_")
        group.owner_id=self.request.user.pk
        group.save()

        tasks.send_message_about_group.delay(group.name, group.slug, self.request.user.email)
        return redirect(group)


class DetailGroupView(DataMixin, SingleObjectMixin, ListView):
    """Detail group page"""

    template_name = 'main/detail_group.html'
    paginate_by = 3
    slug_url_kwarg = 'group_slug'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Group.objects.all().prefetch_related('followers').select_related('owner'))
        self.followers = self.object.followers.all()
        self.publication = Publication.objects.filter(group_id=self.object.id).select_related('owner').annotate(
            rat=Avg('rating__star_id')).order_by('-date')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['group'] = self.object
        context['followers'] = self.followers
        return context | self.get_context()

    def get_queryset(self):
        return self.publication


class AddPublication(DataMixin, CreateView):
    """Page for creating new publication"""

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

            tasks.send_message_about_published.delay(published.name, published.slug, request.user.email)
            return redirect(group)
        return super().post(request, *args, **kwargs)


class DetailPublication(DataMixin, DetailView):
    """Detail publish page"""

    model = Publication
    slug_url_kwarg = 'publish_slug'
    template_name = 'main/detail_publish.html'
    context_object_name = "publication"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(
            Publication.objects.all().select_related('group', 'owner').annotate(rat=Avg('rating__star_id'))
        )
        self.rating = Rating.objects.filter(publication_id__name=self.object.name).select_related('star').filter(
            ip=self.request.user.username)
        
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['star_form'] = RatingForm()

        if self.request.user.is_authenticated:
            context['rating'] = self.rating[0] if self.rating else None

        return context | self.get_context()


class PublicationCommentsView(SingleObjectMixin, ListView):
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
        context['title'] = 'Comments'
        context['menu'] = menu
        context['publication'] = self.object
        return context

    def get_queryset(self):
        return self.comments


# Logic
def del_group(request, group_slug):
    """Delete group for owner"""

    Group.objects.get(slug=group_slug).delete()
    return redirect(reverse('groups', kwargs={'user_pk': request.user.pk}))


def delete_publication(request, pub_id: int) -> HttpResponse:
    """Delete publication"""

    Publication.objects.get(id=pub_id).delete()
    return HttpResponse(status=204)


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


def group_activity(request, group_id: int) -> HttpResponse:
    """Join to the group or leave the group"""

    q = Group.objects.prefetch_related('followers').get(id=group_id)
    if request.user in q.followers.all():
        q.followers.remove(request.user)
    else:
        q.followers.add(request.user)

    return HttpResponse(status=200)


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
