from django.db.models import Avg
from django.urls import reverse
from django.test import TestCase
from django.core.exceptions import PermissionDenied


from src.main.models import Publication, Group, Comment, Rating, RatingStar

from src.users.models import User, Follower, Chat, Message


class NewsViewTest(TestCase):
    """Testing the NewsView class methods"""

    fixtures = ["./config/tests/test_data.json"]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.publication_1 = Publication.objects.get(pk=1)
        cls.publication_2 = Publication.objects.get(pk=2)

        cls.pub_1_rating = cls.publication_1.rating_set.all()
        cls.pub_2_rating = cls.publication_2.rating_set.all()

    def test_view_url(self):
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
        assert request.status_code == 200, request.status_code
        assert len(self.pub_1_rating) == 0, self.pub_1_rating
        assert len(self.pub_2_rating) == 0, self.pub_2_rating


class HomeViewTest(TestCase):
    """Testing the HomeView class methods"""

    fixtures = ["./config/tests/test_data.json"]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_1 = User.objects.get(id=1)
        cls.user_2 = User.objects.get(id=2)
        cls.user_3 = User.objects.get(id=3)

        cls.follower_1 = Follower.objects.get(id=1)
        cls.follower_2 = Follower.objects.get(id=2)
        cls.follower_3 = Follower.objects.get(id=3)
        
        cls.publication_1 = Publication.objects.get(id=1)
        cls.publication_2 = Publication.objects.get(id=2)

        cls.pub_1_rating = cls.publication_1.rating_set.all()
        cls.pub_2_rating = cls.publication_2.rating_set.all()
    
    def test_view_url(self):
        request = self.client.get(reverse('home', kwargs={'user_pk': self.user_3.pk}))
        assert request.status_code == 302, request.status_code

        request = self.client.get(reverse('home', kwargs={'user_pk': self.user_3.pk}), follow=True)
        assert request.status_code == 200, request.status_code
        self.assertTemplateUsed(request, 'users/login.html')

        self.client.login(username='lanterman', password='karmavdele')
        request = self.client.get(reverse('home', kwargs={'user_pk': self.user_3.pk}))
        assert request.status_code == 200, request.status_code
        assert len(request.templates) == 6, request.templates

    def test_user_followers(self):
        self.client.login(username='lanterman', password='karmavdele')
        request = self.client.get(reverse('home', kwargs={'user_pk': self.user_3.pk}))
        assert request.status_code == 200, request.status_code
        assert len(request.context["subs"]) == 1, len(request.context["subs"])
        assert len(request.context["followers"]) == 1, len(request.context["followers"])
        assert len(request.context["new_followers"]) == 1, len(request.context["new_followers"])

    def test_publication_rating(self):
        self.client.login(username='lanterman', password='karmavdele')
        request = self.client.get(reverse('home', kwargs={'user_pk': self.user_3.pk}))
        assert request.status_code == 200, request.status_code
        assert len(self.pub_1_rating) == 0, self.pub_1_rating
        assert len(self.pub_2_rating) == 0, self.pub_2_rating

    def test_context_if_logged_in(self):
        self.client.login(username='lanterman', password='karmavdele')
        request = self.client.get(reverse('home', kwargs={'user_pk': self.user_3.pk}))
        assert "user" in request.context, request.context
        assert request.context["user"].__str__() == "lanterman", request.context["user"]

    def test_context_if_not_logged_in(self):
        request = self.client.get(reverse('home', kwargs={'user_pk': self.user_3.pk}))
        self.assertRedirects(request, f'/users/login/?next=/home/{self.user_3.id}/')
        self.assertFalse(request.context)

    def test_redirect(self):
        resp = self.client.get(reverse('home', kwargs={'user_pk': self.user_3.id}))
        self.assertRedirects(resp, f'/users/login/?next=/home/{self.user_3.id}/')


class MessagesViewTest(TestCase):
    """Testing the MessagesView class methods"""

    fixtures = ["./config/tests/test_data.json"]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_1 = User.objects.get(id=1)
        cls.user_2 = User.objects.get(id=2)
        cls.user_3 = User.objects.get(id=3)

        cls.chat_1 = Chat.objects.get(id=1)
        cls.chat_2 = Chat.objects.get(id=2)

    def test_view_url(self):
        request = self.client.get(reverse('messages', kwargs={'user_pk': self.user_3.pk}))
        assert request.status_code == 302, request.status_code

        request = self.client.get(reverse('messages', kwargs={'user_pk': self.user_3.pk}), follow=True)
        assert request.status_code == 200, request.status_code
        self.assertTemplateUsed(request, 'users/login.html')

        self.client.login(username='lanterman', password='karmavdele')
        request = self.client.get(reverse('messages', kwargs={'user_pk': self.user_3.pk}))
        assert request.status_code == 200, request.status_code
        assert len(request.templates) == 4, request.templates

    def test_chat_members(self):
        self.client.login(username='lanterman', password='karmavdele')
        request = self.client.get(reverse('messages', kwargs={'user_pk': self.user_3.pk}))
        assert request.status_code == 200, request.status_code
        assert len(request.context["chats"]) == 1, request.context["chats"]
        assert self.chat_1 not in request.context["chats"], request.context["chats"]
        assert self.chat_2 in request.context["chats"], request.context["chats"]

    def test_context_if_logged_in(self):
        self.client.login(username='lanterman', password='karmavdele')
        request = self.client.get(reverse('messages', kwargs={'user_pk': self.user_3.pk}))
        assert request.context["title"] == "My messages", request.context["title"]
        assert "user" in request.context, request.context
        assert request.context["user"].__str__() == "lanterman", request.context["user"]

    def test_context_if_not_logged_in(self):
        request = self.client.get(reverse('messages', kwargs={'user_pk': self.user_3.pk}))
        self.assertRedirects(request, f'/users/login/?next=/messages/{self.user_3.id}/')
        self.assertFalse(request.context)

    def test_redirect(self):
        resp = self.client.get(reverse('messages', kwargs={'user_pk': self.user_3.id}))
        self.assertRedirects(resp, f'/users/login/?next=/messages/{self.user_3.id}/')


class ChatDetailViewTest(TestCase):
    """Testing the ChatDetailView class methods"""

    fixtures = ["./config/tests/test_data.json"]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_1 = User.objects.get(id=1)
        cls.user_2 = User.objects.get(id=2)
        cls.user_3 = User.objects.get(id=3)

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


# class CreateDialogViewTest(TestCase):

#     @classmethod
#     def setUpTestData(cls):
#         for user_num in range(3):
#             Users.objects.create(username='user_%s' % user_num, first_name='user_%s' % user_num,
#                                  last_name='user_%s' % user_num, num_tel=12345678910,
#                                  email='user_%s@mail.ru' % user_num)
#         chat = [Chat.objects.create() for n in range(2)]
#         users = Users.objects.all()
#         chat[0].members.add(users[0], users[1])
#         chat[1].members.add(users[1], users[2])

#     def test_chat(self):
#         chat = Chat.objects.all()
#         users = Users.objects.all()
#         self.assertTrue(users[2] in chat[1].members.all())
#         self.assertFalse(users[2] in chat[0].members.all())
#         self.assertEqual(users[1] in chat[0].members.all(), users[0] in chat[0].members.all())


# class FriendsViewTest(TestCase):

#     @classmethod
#     def setUpTestData(cls):
#         for user_num in range(3):
#             Users.objects.create_user(username='user_%s' % user_num, password='12345', num_tel=12345678910,
#                                       email='user_%s@mail.ru' % user_num)

#     def test_view_url(self):
#         user = Users.objects.get(username='user_1')
#         resp = self.client.get(reverse('friends', kwargs={'user_pk': user.pk}), follow=True)
#         self.assertEqual(resp.status_code, 200)

#     def test_view_template(self):
#         self.client.login(username='user_1', password='12345')
#         user = Users.objects.get(username='user_1')
#         resp = self.client.get(f'/friends/{user.pk}/')
#         self.assertEqual(resp.status_code, 200)
#         self.assertTemplateUsed(resp, 'main/friends.html')

#     def test_context_if_logged_in(self):
#         self.client.login(username='user_1', password='12345')
#         user = Users.objects.get(username='user_1')
#         resp = self.client.get(f'/friends/{user.pk}/')
#         self.assertEqual(str(resp.context['user']), 'user_1')
#         self.assertTrue('title' in resp.context)
#         self.assertEqual(resp.context['title'], 'Мои друзья')

#     def test_context_if_not_logged_in(self):
#         user = Users.objects.get(username='user_1')
#         resp = self.client.get(f'/friends/{user.pk}/')
#         self.assertRedirects(resp, f'/users/login/?next=/friends/{user.pk}/')
#         self.assertFalse(resp.context)

#     def test_redirect(self):
#         user = Users.objects.get(username='user_1')
#         resp = self.client.get(f'/friends/{user.pk}/')
#         self.assertRedirects(resp, f'/users/login/?next=/friends/{user.pk}/')


# class GroupsViewTest(TestCase):

#     @classmethod
#     def setUpTestData(cls):
#         Groups.objects.create(name='group', slug='group')
#         Users.objects.create_user(username='testuser1', password='12345', first_name='user1', last_name='user1',
#                                   num_tel=12345678910, email='test1@mail.ru', slug='user1')

#     def test_view_url(self):
#         user = Users.objects.get(username='testuser1')
#         resp = self.client.get(reverse('groups', kwargs={'user_pk': user.pk}), follow=True)
#         self.assertEqual(resp.status_code, 200)

#     def test_view_template(self):
#         self.client.login(username='testuser1', password='12345')
#         user = Users.objects.get(username='testuser1')
#         resp = self.client.get(f'/groups/{user.pk}/')
#         self.assertEqual(resp.status_code, 200)
#         self.assertTemplateUsed(resp, 'main/groups.html')

#     def test_context_if_logged_in(self):
#         self.client.login(username='testuser1', password='12345')
#         user = Users.objects.get(username='testuser1')
#         resp = self.client.get(f'/groups/{user.pk}/')
#         self.assertEqual(str(resp.context['user']), 'testuser1')
#         self.assertTrue('title' in resp.context)
#         self.assertEqual(resp.context['title'], 'Мои группы')

#     def test_context_if_not_logged_in(self):
#         user = Users.objects.get(username='testuser1')
#         resp = self.client.get(f'/groups/{user.pk}/')
#         self.assertRedirects(resp, f'/users/login/?next=/groups/{user.pk}/')
#         self.assertFalse(resp.context)

#     def test_redirect(self):
#         user = Users.objects.get(username='testuser1')
#         resp = self.client.get(f'/groups/{user.pk}/')
#         self.assertRedirects(resp, f'/users/login/?next=/groups/{user.pk}/')


# class AddGroupTest(TestCase):

#     @classmethod
#     def setUpTestData(cls):
#         Groups.objects.create(name='group', slug='group')
#         Users.objects.create_user(username='testuser1', password='12345', first_name='user1', last_name='user1',
#                                   num_tel=12345678910, email='test1@mail.ru', slug='user1')

#     def test_view_url(self):
#         resp = self.client.get(reverse('add_group'), follow=True)
#         self.assertEqual(resp.status_code, 200)

#     def test_view_template(self):
#         self.client.login(username='testuser1', password='12345')
#         resp = self.client.get('/groups/add_group/')
#         self.assertEqual(resp.status_code, 200)
#         self.assertTemplateUsed(resp, 'main/add_pub_group.html')

#     def test_context_if_logged_in(self):
#         self.client.login(username='testuser1', password='12345')
#         resp = self.client.get('/groups/add_group/')
#         self.assertEqual(str(resp.context['user']), 'testuser1')
#         self.assertTrue('title' in resp.context)
#         self.assertEqual(resp.context['title'], 'Создать группу')

#     def test_context_if_not_logged_in(self):
#         resp = self.client.get('/groups/add_group/')
#         self.assertRedirects(resp, f'/users/login/?next=/groups/add_group/')
#         self.assertFalse(resp.context)

#     def test_redirect(self):
#         resp = self.client.get('/groups/add_group/')
#         self.assertRedirects(resp, f'/users/login/?next=/groups/add_group/')


# class DetailGroupViewTest(TestCase):

#     @classmethod
#     def setUpTestData(cls):
#         group = Groups.objects.create(name='group_1', slug='group_1')
#         Groups.objects.create(name='group_2', slug='group_2')
#         for user_num in range(2):
#             Users.objects.create_user(username='user_%s' % user_num, password='12345', num_tel=12345678910,
#                                       email='user_%s@mail.ru' % user_num)
#         user = Users.objects.get(username='user_1')
#         group.users.add(user)
#         Published.objects.create(name='pub_1', slug='pub_1', group=group)

#     def test_view_url(self):
#         group = Groups.objects.get(name='group_1')
#         resp = self.client.get(reverse('detail_group', kwargs={'group_slug': group.slug}), follow=True)
#         self.assertEqual(resp.status_code, 200)

#     def test_group_and_user(self):
#         group = Groups.objects.all()
#         users = Users.objects.all()
#         self.assertEqual(group[0].users.count() == 1, group[1].users.count() == 0)
#         self.assertEqual(users[0].groups_users.count() == 1, users[1].groups_users.count() == 0)

#     def test_published_rating(self):
#         published = Published.objects.annotate(rat=Avg('rating__star_id')).order_by('-date').get(name='pub_1')
#         self.assertEqual(published.rat, None)

#     def test_view_template(self):
#         self.client.login(username='user_1', password='12345')
#         group = Groups.objects.get(name='group_1')
#         resp = self.client.get(reverse('detail_group', kwargs={'group_slug': group.slug}))
#         self.assertEqual(resp.status_code, 200)
#         self.assertTemplateUsed(resp, 'main/detail_group.html')

#     def test_context_if_not_logged_in(self):
#         group = Groups.objects.get(name='group_1')
#         resp = self.client.get(reverse('detail_group', kwargs={'group_slug': group.slug}))
#         self.assertRedirects(resp, f'/users/login/?next=/groups/{group.slug}/')
#         self.assertFalse(resp.context)

#     def test_redirect(self):
#         group = Groups.objects.get(name='group_1')
#         resp = self.client.get(f'/groups/{group.slug}/')
#         self.assertRedirects(resp, f'/users/login/?next=/groups/{group.slug}/')


# class AddPublishedTest(TestCase):

#     @classmethod
#     def setUpTestData(cls):
#         group = Groups.objects.create(name='group', slug='group')
#         Users.objects.create_user(username='testuser1', password='12345', first_name='user1', last_name='user1',
#                                   num_tel=12345678910, email='test1@mail.ru', slug='user1')
#         Published.objects.create(name='pub', slug='pub', group=group)

#     def test_view_url(self):
#         group = Groups.objects.get(name='group')
#         resp = self.client.get(reverse('add_published', kwargs={'group_slug': group.slug}), follow=True)
#         self.assertEqual(resp.status_code, 200)

#     def test_view_template(self):
#         self.client.login(username='testuser1', password='12345')
#         group = Groups.objects.get(name='group')
#         resp = self.client.get(reverse('add_published', kwargs={'group_slug': group.slug}))
#         self.assertEqual(resp.status_code, 200)
#         self.assertTemplateUsed(resp, 'main/add_pub_group.html')

#     def test_context_if_logged_in(self):
#         self.client.login(username='testuser1', password='12345')
#         group = Groups.objects.get(name='group')
#         resp = self.client.get(reverse('add_published', kwargs={'group_slug': group.slug}))
#         self.assertEqual(str(resp.context['user']), 'testuser1')
#         self.assertTrue('title' in resp.context)
#         self.assertEqual(resp.context['title'], 'Создать запись')

#     def test_context_if_not_logged_in(self):
#         group = Groups.objects.get(name='group')
#         resp = self.client.get(reverse('add_published', kwargs={'group_slug': group.slug}))
#         self.assertRedirects(resp, f'/users/login/?next=/groups/{group.slug}/add_published/')
#         self.assertFalse(resp.context)

#     def test_redirect(self):
#         group = Groups.objects.get(name='group')
#         resp = self.client.get(reverse('add_published', kwargs={'group_slug': group.slug}))
#         self.assertRedirects(resp, f'/users/login/?next=/groups/{group.slug}/add_published/')


# class DetailPublishTest(TestCase):

#     @classmethod
#     def setUpTestData(cls):
#         Users.objects.create_user(username='testuser1', password='12345', first_name='user1', last_name='user1',
#                                   num_tel=12345678910, email='test1@mail.ru', slug='user1')
#         group = Groups.objects.create(name='group_1', slug='group_1')
#         Published.objects.create(name='pub_1', slug='pub_1', group=group)

#     def test_view_url(self):
#         pub = Published.objects.get(name='pub_1')
#         resp = self.client.get(reverse('detail_publish', kwargs={'publish_slug': pub.slug}))
#         self.assertEqual(resp.status_code, 200)

#     def test_published_rating(self):
#         published = Published.objects.annotate(rat=Avg('rating__star_id')).order_by('-date').get(name='pub_1')
#         self.assertEqual(published.rat, None)

#     def test_view_template(self):
#         pub = Published.objects.get(name='pub_1')
#         resp = self.client.get(f'/publish/{pub.slug}/')
#         self.assertEqual(resp.status_code, 200)
#         self.assertTemplateUsed(resp, 'main/detail_publish.html')

#     def test_if_logged_in(self):
#         self.client.login(username='testuser1', password='12345')
#         pub = Published.objects.get(name='pub_1')
#         resp = self.client.get(f'/publish/{pub.slug}/')
#         self.assertEqual(str(resp.context['user']), 'testuser1')


# class PublishedCommentsViewTest(TestCase):

#     @classmethod
#     def setUpTestData(cls):
#         user = Users.objects.create_user(username='testuser1', password='12345', first_name='user1', last_name='user1',
#                                          num_tel=12345678910, email='test1@mail.ru', slug='user1')
#         group = Groups.objects.create(name='group_1', slug='group_1')
#         pub = Published.objects.create(name='pub_1', slug='pub_1', group=group)
#         for com_num in range(7):
#             Comments.objects.create(published=pub, users=user, biography='why_%s???' % com_num)

#     def test_view_url(self):
#         publish = Published.objects.get(name='pub_1')
#         resp = self.client.get(reverse('comments', kwargs={'publish_slug': publish.slug}))
#         self.assertEqual(resp.status_code, 200)

#     def test_view_template(self):
#         publish = Published.objects.get(name='pub_1')
#         resp = self.client.get(reverse('comments', kwargs={'publish_slug': publish.slug}))
#         self.assertEqual(resp.status_code, 200)
#         self.assertTemplateUsed(resp, 'main/comments.html')

#     def test_context_if_logged_in(self):
#         self.client.login(username='testuser1', password='12345')
#         publish = Published.objects.get(name='pub_1')
#         resp = self.client.get(reverse('comments', kwargs={'publish_slug': publish.slug}))
#         self.assertEqual(str(resp.context['user']), 'testuser1')
#         self.assertTrue('title' in resp.context)
#         self.assertEqual(resp.context['title'], 'Комментарии')


# class DelGroupTest(TestCase):

#     @classmethod
#     def setUpTestData(cls):
#         Groups.objects.create(name='group', slug='group')
#         Users.objects.create(username='user', first_name='user', last_name='user', num_tel=12345678910,
#                              email='user@mail.ru')

#     def test_view_url(self):
#         user = Users.objects.get(username='user')
#         resp = self.client.get(reverse('groups', kwargs={'user_pk': user.pk}), follow=True)
#         self.assertEqual(resp.status_code, 200)

#     def test_del_group(self):
#         group = Groups.objects.filter(name='group')
#         self.assertEqual(group.count(), 1)
#         Groups.objects.get(slug='group').delete()
#         self.assertEqual(group.count(), 0)


# class DelPubGroupTest(TestCase):

#     @classmethod
#     def setUpTestData(cls):
#         group = Groups.objects.create(name='group', slug='group')
#         Published.objects.create(name='pub_1', slug='pub_1', group=group)

#     def test_view_url(self):
#         group = Groups.objects.get(name='group')
#         resp = self.client.get(reverse('detail_group', kwargs={'group_slug': group.slug}), follow=True)
#         self.assertEqual(resp.status_code, 200)

#     def test_del_pub_group(self):
#         pub = Published.objects.filter(name='pub_1')
#         self.assertTrue(pub.count() == 1)
#         pub.delete()
#         self.assertTrue(pub.count() == 0)


# class DelPublishedTest(TestCase):

#     @classmethod
#     def setUpTestData(cls):
#         group = Groups.objects.create(name='group', slug='group')
#         Published.objects.create(name='pub_1', slug='pub_1', group=group)
#         Users.objects.create(username='user', first_name='user', last_name='user', num_tel=12345678910,
#                              email='user@mail.ru')

#     def test_view_url(self):
#         user = Users.objects.get(username='user')
#         resp = self.client.get(reverse('home', kwargs={'user_pk': user.pk}), follow=True)
#         self.assertEqual(resp.status_code, 200)

#     def test_del_pub_group(self):
#         pub = Published.objects.filter(name='pub_1')
#         self.assertTrue(pub.count() == 1)
#         pub.delete()
#         self.assertTrue(pub.count() == 0)


# class FriendActivityTest(TestCase):

#     @classmethod
#     def setUpTestData(cls):
#         for user_num in range(1, 4):
#             Users.objects.create(username='user_%s' % user_num, first_name='user_%s' % user_num,
#                                  last_name='user_%s' % user_num, num_tel=12345678910,
#                                  email='user_%s@mail.ru' % user_num)
#         users = Users.objects.all()
#         users[0].friends.add(users[1])
#         PostSubscribers.objects.create(owner='user_2', user=users[0])

#     def test_view_url(self):
#         user = Users.objects.get(username='user_1')
#         resp = self.client.get(reverse('home', kwargs={'user_pk': user.pk}), follow=True)
#         self.assertEqual(resp.status_code, 200)

#     def test_del_friend(self):
#         users = Users.objects.all()
#         post = PostSubscribers.objects.filter(owner=users[0].username)
#         self.assertEqual(users[0].friends.count() == 1, post.count() == 0)
#         users[0].friends.remove(users[1])
#         post.create(owner=users[0].username, user_id=users[1].id)
#         self.assertEqual(users[0].friends.count() == 0, post.count() == 1)

#     def test_create_subs(self):
#         users = Users.objects.all()
#         post = PostSubscribers.objects.filter(owner=users[0].username)
#         self.assertEqual(post.count(), 0)
#         post.create(owner=users[0].username, user_id=users[1].id)
#         self.assertEqual(post.count(), 1)

#     def test_add_friend(self):
#         users = Users.objects.all()
#         post = PostSubscribers.objects.all()
#         self.assertEqual(post.count() == 1, users[2].friends.count() == 0)
#         users[2].friends.add(users[0])
#         post.delete()
#         self.assertEqual(post.count() == 0, users[2].friends.count() == 1)

#     def test_del_post(self):
#         post = PostSubscribers.objects.all()
#         self.assertEqual(post.count(), 1)
#         post.delete()
#         self.assertEqual(post.count(), 0)


# class FriendHideTest(TestCase):

#     @classmethod
#     def setUpTestData(cls):
#         user = Users.objects.create(username='user', first_name='user', last_name='user', num_tel=12345678910)
#         PostSubscribers.objects.create(owner='user_2', user=user)

#     def test_view_url(self):
#         user = Users.objects.get(username='user')
#         resp = self.client.get(reverse('home', kwargs={'user_pk': user.pk}), follow=True)
#         self.assertEqual(resp.status_code, 200)

#     def test_del_post(self):
#         post = PostSubscribers.objects.filter(owner='user_2')
#         self.assertFalse(post[0].escape)
#         post.update(escape=True)
#         self.assertTrue(post[0].escape)


# class FriendAcceptTest(TestCase):

#     @classmethod
#     def setUpTestData(cls):
#         for user_num in range(1, 3):
#             Users.objects.create(username='user_%s' % user_num, first_name='user_%s' % user_num,
#                                  last_name='user_%s' % user_num, num_tel=12345678910,
#                                  email='user_%s@mail.ru' % user_num)
#         users = Users.objects.all()
#         PostSubscribers.objects.create(owner=users[1].username, user=users[0])

#     def test_view_url(self):
#         user = Users.objects.get(username='user_1')
#         resp = self.client.get(reverse('home', kwargs={'user_pk': user.pk}), follow=True)
#         self.assertEqual(resp.status_code, 200)

#     def test_add_friend(self):
#         users = Users.objects.all()
#         post = PostSubscribers.objects.all()
#         self.assertEqual(post.count() == 1, users[1].friends.count() == 0)
#         users[1].friends.add(users[0])
#         post.delete()
#         self.assertEqual(post.count() == 0, users[1].friends.count() == 1)


# class FriendDelPrimaryTest(TestCase):

#     @classmethod
#     def setUpTestData(cls):
#         for user_num in range(1, 3):
#             Users.objects.create(username='user_%s' % user_num, first_name='user_%s' % user_num,
#                                  last_name='user_%s' % user_num, num_tel=12345678910,
#                                  email='user_%s@mail.ru' % user_num)
#         users = Users.objects.all()
#         users[0].friends.add(users[1])

#     def test_view_url(self):
#         user = Users.objects.get(username='user_1')
#         resp = self.client.get(reverse('home', kwargs={'user_pk': user.pk}), follow=True)
#         self.assertEqual(resp.status_code, 200)

#     def test_del_friend(self):
#         users = Users.objects.all()
#         post = PostSubscribers.objects.all()
#         self.assertEqual(users[0].friends.count() == 1, post.count() == 0)
#         users[0].friends.remove(users[1])
#         post.create(owner=users[0].username, user_id=users[1].id)
#         self.assertEqual(users[0].friends.count() == 0, post.count() == 1)


# class GroupActivityTest(TestCase):

#     @classmethod
#     def setUpTestData(cls):
#         Users.objects.create(username='user', first_name='user', last_name='user', num_tel=123456789, email='s@mail.ru')
#         user = Users.objects.create(username='user2', first_name='user2', last_name='user2', num_tel=12345678910)
#         group = Groups.objects.create(name='group', slug='group')
#         group.users.add(user)

#     def test_view_url(self):
#         group = Groups.objects.get(name='group')
#         resp = self.client.get(reverse('detail_group', kwargs={'group_slug': group.slug}), follow=True)
#         self.assertEqual(resp.status_code, 200)

#     def test_remove_user(self):
#         user = Users.objects.get(username='user2')
#         group = Groups.objects.get(name='group')
#         self.assertEqual(group.users.count(), 1)
#         group.users.remove(user)
#         self.assertEqual(group.users.count(), 0)

#     def test_add_user(self):
#         user = Users.objects.get(username='user')
#         group = Groups.objects.get(name='group')
#         self.assertEqual(group.users.count(), 1)
#         group.users.add(user)
#         self.assertEqual(group.users.count(), 2)


# class GroupQuitPrimaryTest(TestCase):

#     @classmethod
#     def setUpTestData(cls):
#         user = Users.objects.create(username='user', first_name='user', last_name='user', num_tel=12345678910)
#         group = Groups.objects.create(name='group', slug='group')
#         group.users.add(user)

#     def test_view_url(self):
#         user = Users.objects.get(username='user')
#         resp = self.client.get(reverse('groups', kwargs={'user_pk': user.pk}), follow=True)
#         self.assertEqual(resp.status_code, 200)

#     def test_remove_user(self):
#         user = Users.objects.get(username='user')
#         group = Groups.objects.get(name='group')
#         self.assertEqual(group.users.count(), 1)
#         group.users.remove(user)
#         self.assertEqual(group.users.count(), 0)


# class LikeViewTest(TestCase):

#     @classmethod
#     def setUpTestData(cls):
#         Users.objects.create(username='user', first_name='user', last_name='user', num_tel=123456789, email='s@mail.ru')
#         user = Users.objects.create(username='user2', first_name='user2', last_name='user2', num_tel=12345678910)
#         group = Groups.objects.create(name='group', slug='group')
#         pub = Published.objects.create(name='pub', slug='pub', group=group)
#         comment = Comments.objects.create(published=pub, users=user, biography='why???')
#         comment.like.add(user)

#     def test_view_url(self):
#         publish = Published.objects.get(name='pub')
#         resp = self.client.get(reverse('comments', kwargs={'publish_slug': publish.slug}))
#         self.assertEqual(resp.status_code, 200)

#     def test_remove_user(self):
#         user = Users.objects.get(username='user2')
#         comment = Comments.objects.get(biography='why???')
#         self.assertEqual(comment.like.count(), 1)
#         comment.like.remove(user)
#         self.assertEqual(comment.like.count(), 0)

#     def test_add_user(self):
#         user = Users.objects.get(username='user')
#         comment = Comments.objects.get(biography='why???')
#         self.assertEqual(comment.like.count(), 1)
#         comment.like.add(user)
#         self.assertEqual(comment.like.count(), 2)
