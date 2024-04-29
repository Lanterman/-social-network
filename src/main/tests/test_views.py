from django.urls import reverse
from django.test import TestCase

from src.main.models import Publication, Group, Rating

from src.users.models import User, Chat, Message


class NewsViewTest(TestCase):
    """Testing theendpoint"""

    fixtures = ["./config/tests/test_data.json"]

    def test_view_url(self):
        request = self.client.get('')
        assert request.status_code == 200, request.status_code

        self.client.login(username='lanterman', password='karmavdele')
        request = self.client.get('')
        assert request.status_code == 200, request.status_code

    def test_view_template(self):
        request = self.client.get(reverse('news'))
        assert request.status_code == 200, request.status_code
        self.assertTemplateUsed(request, 'main/index.html')

    def test_pagination(self):
        request = self.client.get(reverse('news'))
        assert request.status_code == 200, request.status_code
        assert "is_paginated" in request.context, request.context
        assert len(request.context['page_obj']) == 2, len(request.context['page_obj'])

    def test_lists_all_pub(self):
        with self.assertLogs(level="WARNING"):
            request = self.client.get(reverse('news') + '?page=2')
        
        context = request.context
        assert request.status_code == 404, request.status_code
        assert "exception" in context, context
        assert context['exception'] == "Invalid page (2): That page contains no results", context['exception']

    def test_publication_rating(self):
        request = self.client.get(reverse('news'))
        page_obj = request.context["page_obj"]
        assert request.status_code == 200, request.status_code
        assert len(page_obj) == 2, page_obj
        assert page_obj[0].__str__() == "Second publication", page_obj[0].__str__()
        assert page_obj[1].__str__() == "publication", page_obj[1].__str__()
        assert page_obj[0].rat == None, page_obj[0].rat
        assert page_obj[1].rat == None, page_obj[1].rat

class HomeViewTest(TestCase):
    """Testing the Homeendpoint"""

    fixtures = ["./config/tests/test_data.json"]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.get(id=3)
    
    def test_view_url(self):
        request = self.client.get(reverse('home', kwargs={'user_pk': self.user.pk}))
        assert request.status_code == 302, request.status_code

        request = self.client.get(reverse('home', kwargs={'user_pk': self.user.pk}), follow=True)
        assert request.status_code == 200, request.status_code
        self.assertTemplateUsed(request, 'users/login.html')

        self.client.login(username='lanterman', password='karmavdele')
        request = self.client.get(reverse('home', kwargs={'user_pk': self.user.pk}))
        assert request.status_code == 200, request.status_code
        assert len(request.templates) == 7, request.templates

    def test_user_followers(self):
        self.client.login(username='lanterman', password='karmavdele')
        request = self.client.get(reverse('home', kwargs={'user_pk': self.user.pk}))
        assert request.status_code == 200, request.status_code
        assert len(request.context["subs"]) == 1, len(request.context["subs"])
        assert len(request.context["followers"]) == 1, len(request.context["followers"])
        assert len(request.context["new_followers"]) == 1, len(request.context["new_followers"])
    
    def test_profile_of_other_user(self):
        self.client.login(username='admin', password='admin')
        request = self.client.get(reverse('home', kwargs={'user_pk': self.user.pk}))
        assert request.status_code == 200, request.status_code
        assert len(request.context["subs"]) == 1, len(request.context["subs"])
        assert request.context["user"].__str__() == "lanterman", request.context["user"]
        assert request.context["i_am_follower"] == True, request.context["i_am_follower"]
        assert request.context["i_am_sub"] == True, request.context["i_am_sub"]

    def test_publication_rating(self):
        request = self.client.get(reverse('news'))
        page_obj = request.context["page_obj"]
        assert request.status_code == 200, request.status_code
        assert len(page_obj) == 2, page_obj
        assert page_obj[0].__str__() == "Second publication", page_obj[0].__str__()
        assert page_obj[1].__str__() == "publication", page_obj[1].__str__()
        assert page_obj[0].rat == None, page_obj[0].rat
        assert page_obj[1].rat == None, page_obj[1].rat

    def test_context_if_logged_in(self):
        self.client.login(username='lanterman', password='karmavdele')
        request = self.client.get(reverse('home', kwargs={'user_pk': self.user.pk}))
        assert "user" in request.context, request.context
        assert request.context["user"].__str__() == "lanterman", request.context["user"]

    def test_context_if_not_logged_in(self):
        request = self.client.get(reverse('home', kwargs={'user_pk': self.user.pk}))
        self.assertRedirects(request, f'/users/login/?next=/home/{self.user.id}/')
        self.assertFalse(request.context)

    def test_redirect(self):
        resp = self.client.get(reverse('home', kwargs={'user_pk': self.user.id}))
        self.assertRedirects(resp, f'/users/login/?next=/home/{self.user.id}/')


class MessagesViewTest(TestCase):
    """Testing the Messagesendpoint"""

    fixtures = ["./config/tests/test_data.json"]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.get(id=3)

        cls.chat_1 = Chat.objects.get(id=1)
        cls.chat_2 = Chat.objects.get(id=2)

    def test_view_url(self):
        request = self.client.get(reverse('messages', kwargs={'user_pk': self.user.pk}))
        assert request.status_code == 302, request.status_code

        request = self.client.get(reverse('messages', kwargs={'user_pk': self.user.pk}), follow=True)
        assert request.status_code == 200, request.status_code
        self.assertTemplateUsed(request, 'users/login.html')

        self.client.login(username='lanterman', password='karmavdele')
        request = self.client.get(reverse('messages', kwargs={'user_pk': self.user.pk}))
        assert request.status_code == 200, request.status_code
        assert len(request.templates) == 4, request.templates

    def test_chat_members(self):
        self.client.login(username='lanterman', password='karmavdele')
        request = self.client.get(reverse('messages', kwargs={'user_pk': self.user.pk}))
        assert request.status_code == 200, request.status_code
        assert len(request.context["chats"]) == 1, request.context["chats"]
        assert self.chat_1 not in request.context["chats"], request.context["chats"]
        assert self.chat_2 in request.context["chats"], request.context["chats"]

    def test_context_if_logged_in(self):
        self.client.login(username='lanterman', password='karmavdele')
        request = self.client.get(reverse('messages', kwargs={'user_pk': self.user.pk}))
        assert request.context["title"] == "My messages", request.context["title"]
        assert "user" in request.context, request.context
        assert request.context["user"].__str__() == "lanterman", request.context["user"]

    def test_context_if_not_logged_in(self):
        request = self.client.get(reverse('messages', kwargs={'user_pk': self.user.pk}))
        self.assertRedirects(request, f'/users/login/?next=/messages/{self.user.id}/')
        self.assertFalse(request.context)

    def test_redirect(self):
        resp = self.client.get(reverse('messages', kwargs={'user_pk': self.user.id}))
        self.assertRedirects(resp, f'/users/login/?next=/messages/{self.user.id}/')


class ChatDetailViewTest(TestCase):
    """Testing the ChatDetailView endpoint"""

    fixtures = ["./config/tests/test_data.json"]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.chat_1 = Chat.objects.get(id=1)
        cls.chat_2 = Chat.objects.get(id=2)

        cls.message_1 = Message.objects.get(id=1)
        cls.message_2 = Message.objects.get(id=2)

    def test_view_url(self):
        request = self.client.get(reverse('chat', kwargs={'chat_id': self.chat_2.pk}))
        assert request.status_code == 302, request.status_code

        request = self.client.get(reverse('chat', kwargs={'chat_id': self.chat_2.pk}), follow=True)
        assert request.status_code == 200, request.status_code
        self.assertTemplateUsed(request, 'users/login.html')

        self.client.login(username='lanterman', password='karmavdele')

        with self.assertLogs(level="WARNING"):
            request = self.client.get(reverse('chat', kwargs={'chat_id': self.chat_1.pk}))
        assert request.status_code == 403, request.status_code

        request = self.client.get(reverse('chat', kwargs={'chat_id': self.chat_2.pk}))
        assert request.status_code == 200, request.status_code
        assert len(request.templates) == 4, request.templates

    def test_chat_is_messages(self):
        self.client.login(username='lanterman', password='karmavdele')
        request = self.client.get(reverse('chat', kwargs={'chat_id': self.chat_2.pk}))
        assert request.status_code == 200, request.status_code
        assert len(request.context["messages"]) == 1, request.context["messages"]
        assert self.message_1 not in request.context["messages"], request.context["messages"]
        assert self.message_2 in request.context["messages"], request.context["messages"]
    
    def test_send_message(self):
        count_messages = Message.objects.count()
        assert count_messages == 2, count_messages

        self.client.login(username='lanterman', password='karmavdele')
        request = self.client.post(reverse('chat', kwargs={'chat_id': self.chat_2.pk}), data={"message": "hello"})
        count_messages = Message.objects.count()
        assert request.status_code == 200, request.status_code
        assert count_messages == 3, count_messages
        
    def test_context_if_logged_in(self):
        self.client.login(username='lanterman', password='karmavdele')
        request = self.client.get(reverse('chat', kwargs={'chat_id': self.chat_2.pk}))
        assert request.context["title"] == "My message", request.context["title"]
        assert "user" in request.context, request.context
        assert request.context["user"].__str__() == "lanterman", request.context["user"]

    def test_context_if_not_logged_in(self):
        request = self.client.get(reverse('chat', kwargs={'chat_id': self.chat_2.pk}))
        self.assertRedirects(request, f'/users/login/?next=/chat/{self.chat_2.id}/')
        self.assertFalse(request.context)

    def test_redirect(self):
        request = self.client.get(reverse('chat', kwargs={'chat_id': self.chat_2.pk}))
        self.assertRedirects(request, f'/users/login/?next=/chat/{self.chat_2.id}/')


class CreateDialogViewTest(TestCase):
    """Testing the CreateDialogView endpoint"""

    fixtures = ["./config/tests/test_data.json"]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.get(id=3)

    def test_chat_exists(self):
        self.client.login(username="lanterman", password="karmavdele")
        request = self.client.get(reverse('check', kwargs={'user_id': 1}))
        assert request.status_code == 302, request.status_code
        assert request.context == None, request.context

        request = self.client.get(reverse('check', kwargs={'user_id': 1}), follow=True)
        count_chats = Chat.objects.count()
        assert request.status_code == 200, request.status_code
        assert request.context["title"] == "My message", request.context["title"]
        assert len(request.templates) == 4, len(request.templates)
        assert count_chats == 2, count_chats
    
    def test_chat_does_not_exist(self):
        self.client.login(username="lanterman", password="karmavdele")
        request = self.client.get(reverse('check', kwargs={'user_id': 2}))
        assert request.status_code == 302, request.status_code
        assert request.context == None, request.context

        request = self.client.get(reverse('check', kwargs={'user_id': 2}), follow=True)
        count_chats = Chat.objects.count()
        assert request.status_code == 200, request.status_code
        assert request.context["title"] == "My message", request.context["title"]
        assert len(request.templates) == 3, len(request.templates)
        assert count_chats == 3, count_chats


class FollowersViewTest(TestCase):
    """Testing the FollowersView endpoint"""

    fixtures = ["./config/tests/test_data.json"]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.get(id=3)

    def test_view_url(self):
        request = self.client.get(reverse('followers', kwargs={'user_pk': self.user.pk}))
        assert request.status_code == 302, request.status_code

        request = self.client.get(reverse('followers', kwargs={'user_pk': self.user.pk}), follow=True)
        assert request.status_code == 200, request.status_code
        self.assertTemplateUsed(request, 'users/login.html')

        self.client.login(username='lanterman', password='karmavdele')
        request = self.client.get(reverse('followers', kwargs={'user_pk': self.user.pk}))
        assert request.status_code == 200, request.status_code
        assert len(request.templates) == 6, request.templates
    
    def test_context_if_logged_in(self):
        self.client.login(username='lanterman', password='karmavdele')
        request = self.client.get(reverse('followers', kwargs={'user_pk': self.user.pk}))
        assert request.context["title"] == "My followers", request.context["title"]
        assert request.context["name"] == "Search followers", request.context["name"]
        assert len(request.context["object_list"]) == 2, request.context["object_list"]
        assert request.context["object_list"][0].__str__() == "user", request.context["object_list"]
        assert request.context["object_list"][1].__str__() == "admin", request.context["object_list"]

    def test_context_if_not_logged_in(self):
        request = self.client.get(reverse('followers', kwargs={'user_pk': self.user.pk}))
        self.assertRedirects(request, f'/users/login/?next=/followers/{self.user.id}/')
        self.assertFalse(request.context)

    def test_redirect(self):
        request = self.client.get(reverse('followers', kwargs={'user_pk': self.user.pk}))
        self.assertRedirects(request, f'/users/login/?next=/followers/{self.user.id}/')


class SubscriptionsViewTest(TestCase):
    """Testing the SubscriptionsView endpoint"""

    fixtures = ["./config/tests/test_data.json"]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.get(id=3)

    def test_view_url(self):
        request = self.client.get(reverse('subscriptions', kwargs={'user_pk': self.user.pk}))
        assert request.status_code == 302, request.status_code

        request = self.client.get(reverse('subscriptions', kwargs={'user_pk': self.user.pk}), follow=True)
        assert request.status_code == 200, request.status_code
        self.assertTemplateUsed(request, 'users/login.html')

        self.client.login(username='lanterman', password='karmavdele')
        request = self.client.get(reverse('subscriptions', kwargs={'user_pk': self.user.pk}))
        assert request.status_code == 200, request.status_code
        assert len(request.templates) == 5, request.templates
    
    def test_context_if_logged_in(self):
        self.client.login(username='lanterman', password='karmavdele')
        request = self.client.get(reverse('subscriptions', kwargs={'user_pk': self.user.pk}))
        assert request.context["title"] == "My subscriptions", request.context["title"]
        assert request.context["name"] == "Search users", request.context["name"]
        assert len(request.context["object_list"]) == 1, request.context["object_list"]
        assert request.context["object_list"][0].__str__() == "admin", request.context["object_list"]

    def test_context_if_not_logged_in(self):
        request = self.client.get(reverse('subscriptions', kwargs={'user_pk': self.user.pk}))
        self.assertRedirects(request, f'/users/login/?next=/subscriptions/{self.user.id}/')
        self.assertFalse(request.context)

    def test_redirect(self):
        request = self.client.get(reverse('subscriptions', kwargs={'user_pk': self.user.pk}))
        self.assertRedirects(request, f'/users/login/?next=/subscriptions/{self.user.id}/')


class GroupsViewTest(TestCase):
    """Testing the GroupsView endpoint"""

    fixtures = ["./config/tests/test_data.json"]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.get(id=3)
    
    def test_view_url(self):
        request = self.client.get(reverse('groups', kwargs={'user_pk': self.user.pk}))
        assert request.status_code == 302, request.status_code

        request = self.client.get(reverse('groups', kwargs={'user_pk': self.user.pk}), follow=True)
        assert request.status_code == 200, request.status_code
        self.assertTemplateUsed(request, 'users/login.html')

        self.client.login(username='lanterman', password='karmavdele')
        request = self.client.get(reverse('groups', kwargs={'user_pk': self.user.pk}))
        assert request.status_code == 200, request.status_code
        assert len(request.templates) == 5, request.templates
    
    def test_context_if_logged_in(self):
        self.client.login(username='lanterman', password='karmavdele')
        request = self.client.get(reverse('groups', kwargs={'user_pk': self.user.pk}))
        assert request.context["title"] == "My groups", request.context["title"]
        assert request.context["name"] == "Search for groups", request.context["name"]
        assert len(request.context["groups"]) == 1, request.context["groups"]

    def test_context_if_not_logged_in(self):
        request = self.client.get(reverse('groups', kwargs={'user_pk': self.user.pk}))
        self.assertRedirects(request, f'/users/login/?next=/groups/{self.user.id}/')
        self.assertFalse(request.context)

    def test_redirect(self):
        request = self.client.get(reverse('groups', kwargs={'user_pk': self.user.pk}))
        self.assertRedirects(request, f'/users/login/?next=/groups/{self.user.id}/')


class AddGroupTest(TestCase):
    """Testing the AddGroup endpoint"""

    fixtures = ["./config/tests/test_data.json"]
    
    def test_view_url(self):
        request = self.client.get(reverse('add_group'))
        assert request.status_code == 302, request.status_code

        request = self.client.get(reverse('add_group'), follow=True)
        assert request.status_code == 200, request.status_code
        self.assertTemplateUsed(request, 'users/login.html')

        self.client.login(username='lanterman', password='karmavdele')
        request = self.client.get(reverse('add_group'))
        assert request.status_code == 200, request.status_code
        assert len(request.templates) == 15, request.templates
    
    def test_invalid_add_group(self):
        group_info = {"name": "test group@", "photo": "groups/Снимок_экрана_от_2023-12-16_15-37-45.png"}
        self.client.login(username='lanterman', password='karmavdele')

        count_groups = Publication.objects.count()
        assert count_groups == 2, count_groups

        request = self.client.post(reverse('add_group'), data=group_info, follow=True)
        count_groups = Publication.objects.count()
        assert request.status_code == 200, request.status_code
        assert count_groups == 2, count_groups
    
    def test_context_if_logged_in(self):
        self.client.login(username='lanterman', password='karmavdele')
        request = self.client.get(reverse('add_group'))
        assert request.context["title"] == "Create group", request.context["title"]

    def test_context_if_not_logged_in(self):
        request = self.client.get(reverse('add_group'))
        self.assertRedirects(request, f'/users/login/?next=/groups/add_group/')
        self.assertFalse(request.context)

    def test_redirect(self):
        request = self.client.get(reverse('add_group'))
        self.assertRedirects(request, f'/users/login/?next=/groups/add_group/')


class DetailGroupViewTest(TestCase):
    """Testing the DetailGroupView endpoint"""

    fixtures = ["./config/tests/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.group = Group.objects.get(id=1)
    
    def test_view_url(self):
        request = self.client.get(reverse('detail_group', kwargs={'group_slug': self.group.slug}))
        assert request.status_code == 302, request.status_code

        request = self.client.get(reverse('detail_group', kwargs={'group_slug': self.group.slug}), follow=True)
        assert request.status_code == 200, request.status_code
        self.assertTemplateUsed(request, 'users/login.html')

        self.client.login(username='lanterman', password='karmavdele')
        request = self.client.get(reverse('detail_group', kwargs={'group_slug': self.group.slug}))
        assert request.status_code == 200, request.status_code
        assert len(request.templates) == 4, request.templates
    
    def test_context_if_logged_in(self):
        self.client.login(username='lanterman', password='karmavdele')
        request = self.client.get(reverse('detail_group', kwargs={'group_slug': self.group.slug}))
        assert request.context["group"].__str__() == "my group", request.context["group"]

    def test_context_if_not_logged_in(self):
        request = self.client.get(reverse('detail_group', kwargs={'group_slug': self.group.slug}))
        self.assertRedirects(request, f'/users/login/?next=/groups/{self.group.slug}/')
        self.assertFalse(request.context)

    def test_redirect(self):
        request = self.client.get(reverse('detail_group', kwargs={'group_slug': self.group.slug}))
        self.assertRedirects(request, f'/users/login/?next=/groups/{self.group.slug}/')

    def test_group_followers(self):
        self.client.login(username='lanterman', password='karmavdele')
        request = self.client.get(reverse('detail_group', kwargs={'group_slug': self.group.slug}))
        assert len(request.context["followers"]) == 0, request.context["followers"]
    
    def test_publication_rating(self):
        request = self.client.get(reverse('news'))
        page_obj = request.context["page_obj"]
        assert request.status_code == 200, request.status_code
        assert len(page_obj) == 2, page_obj
        assert page_obj[0].__str__() == "Second publication", page_obj[0].__str__()
        assert page_obj[1].__str__() == "publication", page_obj[1].__str__()
        assert page_obj[0].rat == None, page_obj[0].rat
        assert page_obj[1].rat == None, page_obj[1].rat


class AddPublicationTest(TestCase):
    """Testing the AddPublication endpoint"""

    fixtures = ["./config/tests/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.group = Group.objects.get(id=1)
    
    def test_view_url(self):
        request = self.client.get(reverse('add_publication', kwargs={'group_slug': self.group.slug}))
        assert request.status_code == 302, request.status_code

        request = self.client.get(reverse('add_publication', kwargs={'group_slug': self.group.slug}), follow=True)
        assert request.status_code == 200, request.status_code
        self.assertTemplateUsed(request, 'users/login.html')

        self.client.login(username='lanterman', password='karmavdele')
        request = self.client.get(reverse('add_publication', kwargs={'group_slug': self.group.slug}))
        assert request.status_code == 200, request.status_code
        assert len(request.templates) == 21, request.templates
    
    def test_valid_add_publication(self):
        data = {"name": "test pub", "photo": "groups/Снимок_экрана_от_2023-12-16_15-37-45.png", "biography": "biography"}
        self.client.login(username='lanterman', password='karmavdele')

        count_publications = Publication.objects.count()
        assert count_publications == 2, count_publications

        request = self.client.post(reverse('add_publication', kwargs={'group_slug': self.group.slug}), data=data, follow=True)
        count_publications = Publication.objects.count()
        assert request.status_code == 200, request.status_code
        assert count_publications == 3, count_publications
    
    def test_invalid_add_publication(self):
        data = {"name": "test pub@", "photo": "groups/Снимок_экрана_от_2023-12-16_15-37-45.png", "biography": "biography"}
        self.client.login(username='lanterman', password='karmavdele')

        count_publications = Publication.objects.count()
        assert count_publications == 2, count_publications

        request = self.client.post(reverse('add_publication', kwargs={'group_slug': self.group.slug}), data=data, follow=True)
        count_publications = Publication.objects.count()
        assert request.status_code == 200, request.status_code
        assert count_publications == 2, count_publications
    
    def test_context_if_logged_in(self):
        self.client.login(username='lanterman', password='karmavdele')
        request = self.client.get(reverse('add_publication', kwargs={'group_slug': self.group.slug}))
        assert request.context["title"].__str__() == "Create publication", request.context["title"]

    def test_context_if_not_logged_in(self):
        request = self.client.get(reverse('add_publication', kwargs={'group_slug': self.group.slug}))
        self.assertRedirects(request, f'/users/login/?next=/groups/{self.group.slug}/add_publication/')
        self.assertFalse(request.context)

    def test_redirect(self):
        request = self.client.get(reverse('add_publication', kwargs={'group_slug': self.group.slug}))
        self.assertRedirects(request, f'/users/login/?next=/groups/{self.group.slug}/add_publication/')


class DetailPublicationTest(TestCase):
    """Testing the DetailPublication endpoint"""

    fixtures = ["./config/tests/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.publication = Publication.objects.get(id=1)
    
    def test_view_url(self):
        request = self.client.get(reverse('detail_publish', kwargs={'publish_slug': self.publication.slug}))
        assert request.status_code == 302, request.status_code

        request = self.client.get(reverse('detail_publish', kwargs={'publish_slug': self.publication.slug}), follow=True)
        assert request.status_code == 200, request.status_code
        self.assertTemplateUsed(request, 'users/login.html')

        self.client.login(username='lanterman', password='karmavdele')
        request = self.client.get(reverse('detail_publish', kwargs={'publish_slug': self.publication.slug}))
        assert request.status_code == 200, request.status_code
        assert len(request.templates) == 2, request.templates
    
    def test_context_if_logged_in(self):
        self.client.login(username='lanterman', password='karmavdele')
        request = self.client.get(reverse('detail_publish', kwargs={'publish_slug': self.publication.slug}))
        assert request.status_code == 200, request.status_code
        assert request.context["publication"].__str__() == "publication", request.context["publication"]
        assert request.context["publication"].group.__str__() == "my group", request.context["publication"]

    def test_context_if_not_logged_in(self):
        request = self.client.get(reverse('detail_publish', kwargs={'publish_slug': self.publication.slug}))
        self.assertRedirects(request, f'/users/login/?next=/publish/{self.publication.slug}/')
        self.assertFalse(request.context)

    def test_redirect(self):
        request = self.client.get(reverse('detail_publish', kwargs={'publish_slug': self.publication.slug}))
        self.assertRedirects(request, f'/users/login/?next=/publish/{self.publication.slug}/')

    def test_publication_rating(self):
        self.client.login(username='lanterman', password='karmavdele')
        request = self.client.get(reverse('detail_publish', kwargs={'publish_slug': self.publication.slug}))
        assert request.status_code == 200, request.status_code
        assert request.context["rating"] == None, request.context["rating"]


class PublicationCommentsViewTest(TestCase):
    """Testing the PublicationCommentsView endpoint"""

    fixtures = ["./config/tests/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.publication = Publication.objects.get(id=1)
    
    def test_view_url(self):
        request = self.client.get(reverse('comments', kwargs={'publish_slug': self.publication.slug}))
        assert request.status_code == 200, request.status_code
        assert len(request.templates) == 2, request.templates
    
    def test_context(self):
        self.client.login(username='lanterman', password='karmavdele')
        request = self.client.get(reverse('comments', kwargs={'publish_slug': self.publication.slug}))
        assert request.status_code == 200, request.status_code
        assert request.context["title"] == "Comments", request.context["title"]
        assert request.context["publication"].__str__() == "publication", request.context["publication"]


class DelGroupTest(TestCase):
    """Testing the del_group endpoint"""

    fixtures = ["./config/tests/test_data.json"]

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.group_1 = Group.objects.get(id=1)
        cls.group_2 = Group.objects.get(id=2)
    
    def test_view_url(self):
        self.client.login(username="lanterman", password="karmavdele")
        request = self.client.get(reverse('del_group', kwargs={'group_slug': self.group_1.slug}))
        assert request.status_code == 302, request.status_code
        assert request.templates == [], request.templates

        request = self.client.get(reverse('del_group', kwargs={'group_slug': self.group_2.slug}), follow=True)
        assert request.status_code == 200, request.status_code
        assert len(request.templates) == 4, request.templates

    def test_del_group(self):
        self.client.login(username="lanterman", password="karmavdele")
        self.client.get(reverse('del_group', kwargs={'group_slug': self.group_1.slug}), follow=True)
        count_groups = Group.objects.count()
        assert count_groups == 1, count_groups

        self.client.get(reverse('del_group', kwargs={'group_slug': self.group_2.slug}), follow=True)
        count_groups = Group.objects.count()
        assert count_groups == 0, count_groups
    
    def test_context(self):
        self.client.login(username="lanterman", password="karmavdele")
        request = self.client.get(reverse('del_group', kwargs={'group_slug': self.group_1.slug}))
        assert request.status_code == 302, request.status_code
        assert request.context == None, request.context

        request = self.client.get(reverse('del_group', kwargs={'group_slug': self.group_2.slug}), follow=True)
        assert request.status_code == 200, request.status_code
        assert len(request.context["groups"]) == 0, request.context["groups"]
        assert request.context["title"] == "My groups", request.context["title"]
        assert request.context["name"] == "Search for groups", request.context["name"]


class DelPublicationTest(TestCase):
    """Testing the delete_publication endpoint"""

    fixtures = ["./config/tests/test_data.json"]

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.publication_1 = Publication.objects.get(id=1)
        cls.publication_2 = Publication.objects.get(id=2)

    def test_view_url(self):
        request = self.client.get(reverse('delete_publication', kwargs={'pub_id': self.publication_1.id}))
        assert request.status_code == 204, request.status_code
        assert request.templates == [], request.templates

    def test_del_publication(self):
        self.client.get(reverse('delete_publication', kwargs={'pub_id': self.publication_1.id}))
        count_publication = Publication.objects.count()
        assert count_publication == 1, count_publication

        self.client.get(reverse('delete_publication', kwargs={'pub_id': self.publication_2.id}))
        count_publication = Publication.objects.count()
        assert count_publication == 0, count_publication
    
    def test_context(self):
        request = self.client.get(reverse('delete_publication', kwargs={'pub_id': self.publication_1.id}))
        assert request.status_code == 204, request.status_code
        assert request.context == None, request.context


class UpdateGroupTest(TestCase):
    """Testing the UpdateGroup endpoint"""

    fixtures = ["./config/tests/test_data.json"]

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.group = Group.objects.get(id=1)
        cls.data = {"name": "my new name"}

    def test_view_url(self):
        request = self.client.post(reverse('update_group', kwargs={'group_slug': self.group.slug}), data=self.data)
        assert request.status_code == 302, request.status_code
        assert request.templates == [], request.templates

        self.client.login(username="admin", password="admin")
        request = self.client.post(reverse('update_group', kwargs={'group_slug': self.group.slug}), data=self.data, follow=True)
        assert request.status_code == 200, request.status_code
        assert len(request.templates) == 4, len(request.templates)
    
    def test_context(self):
        self.client.login(username="admin", password="admin")
        request = self.client.get(reverse('update_group', kwargs={'group_slug': self.group.slug}))
        assert request.status_code == 200, request.status_code
        assert request.context["title"] == "Change", request.context["title"]
        assert request.context["delete"] == "No", request.context["delete"]


class UpdatePublishedTest(TestCase):
    """Testing the UpdatePublished endpoint"""

    fixtures = ["./config/tests/test_data.json"]

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.pub = Publication.objects.get(id=1)
        cls.data = {"name": "my new name"}

    def test_view_url(self):
        request = self.client.post(reverse('update_pub', kwargs={'pub_slug': self.pub.slug}), data=self.data)
        assert request.status_code == 302, request.status_code
        assert request.templates == [], request.templates

        self.client.login(username="admin", password="admin")
        request = self.client.post(reverse('update_pub', kwargs={'pub_slug': self.pub.slug}), data=self.data, follow=True)
        assert request.status_code == 200, request.status_code
        assert len(request.templates) == 21, len(request.templates)
    
    def test_context(self):
        self.client.login(username="admin", password="admin")
        request = self.client.post(reverse('update_pub', kwargs={'pub_slug': self.pub.slug}), data=self.data)
        assert request.context["title"] == "Change", request.context["title"]
        assert request.context["add"] == "Error!", request.context["add"]

        request = self.client.get(reverse('update_pub', kwargs={'pub_slug': self.pub.slug}))
        assert request.status_code == 200, request.status_code
        assert request.context["title"] == "Change", request.context["title"]
        assert request.context["add"] == "Error!", request.context["add"]


class GroupActivityTest(TestCase):
    """Testing the group_activaity endpoint"""

    fixtures = ["./config/tests/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = User.objects.get(id=3)
        cls.group = Group.objects.get(id=1)

    def test_view_url(self):
        self.client.login(username="lanterman", password="karmavdele")
        request = self.client.get(reverse('group_activity', kwargs={'group_id': self.group.id}))
        assert request.status_code == 200, request.status_code

    def test_remove_user(self):
        self.group.followers.add(self.user)
        count_followers = self.group.followers.count()
        assert count_followers == 1, count_followers

        self.client.login(username="lanterman", password="karmavdele")
        request = self.client.get(reverse('group_activity', kwargs={'group_id': self.group.id}))
        count_followers = self.group.followers.count()
        assert request.status_code == 200, request.status_code
        assert count_followers == 0, count_followers

    def test_add_user(self):
        count_followers = self.group.followers.count()
        assert count_followers == 0, count_followers

        self.client.login(username="lanterman", password="karmavdele")
        request = self.client.get(reverse('group_activity', kwargs={'group_id': self.group.id}))
        count_followers = self.group.followers.count()
        assert request.status_code == 200, request.status_code
        assert count_followers == 1, count_followers


class AddStarRatingTest(TestCase):
    """Testing the AddStarRating endpoint"""

    fixtures = ["./config/tests/test_data.json"]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.data = {"star": 5, "publication": 1}

    def test_view_url(self):
        self.client.login(username="lanterman", password="karmavdele")
        resp = self.client.post(reverse('add_rating'), data=self.data)
        assert resp.status_code == 201, resp.status_code

    def test_create_rating_star(self):
        count_rating_star = Rating.objects.filter(ip="lanterman", publication_id=1).count()
        assert count_rating_star == 0, count_rating_star

        self.client.login(username="lanterman", password="karmavdele")
        request = self.client.post(reverse('add_rating'), data=self.data)
        rating_star = Rating.objects.get(ip="lanterman", publication_id=1)
        assert request.status_code == 201, request.status_code
        assert rating_star.star.value == 5, rating_star.star

    def test_update_rating_star(self):
        Rating.objects.create(ip="lanterman", publication_id_id=1, star_id=1)
        rating_star = Rating.objects.get(ip="lanterman", publication_id=1)
        assert rating_star.star.value == 1, rating_star.star

        self.client.login(username="lanterman", password="karmavdele")
        request = self.client.post(reverse('add_rating'), data=self.data)
        rating_star = Rating.objects.get(ip="lanterman", publication_id=1)
        assert request.status_code == 201, request.status_code
        assert rating_star.star.value == 5, rating_star.star
