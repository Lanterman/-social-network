from django.db.models import Avg
from django.test import TestCase

from main.models import *
from django.urls import reverse

from users.models import *


class NewsViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        for published_num in range(2):
            Groups.objects.create(name='group_%s' % published_num, slug='group_%s' % published_num)
        groups = Groups.objects.all()
        for published_num in range(6):
            Published.objects.create(name='published_%s' % published_num, slug='published_%s' % published_num,
                                     group=groups[0])
        Published.objects.create(name='published_7', slug='published_7', group=groups[1])

    def test_view_url(self):
        resp = self.client.get('')
        self.assertEqual(resp.status_code, 200)

    def test_view_template(self):
        resp = self.client.get(reverse('news'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'main/index.html')

    def test_pagination(self):
        resp = self.client.get(reverse('news'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'])
        self.assertTrue(len(resp.context['page_obj']) == 5)

    def test_lists_all_authors(self):
        resp = self.client.get(reverse('news') + '?page=2')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'])
        self.assertEqual(len(resp.context['page_obj']), 2)

    def test_published_rating(self):
        resp = self.client.get(reverse('news'))
        self.assertEqual(resp.status_code, 200)
        published = Published.objects.all().annotate(rat=Avg('rating__star_id')).order_by('-date')
        pub = published.get(name='published_7')
        self.assertEqual(pub.rat, None)


class HomeViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        for user_num in range(3):
            Users.objects.create(username='user_%s' % user_num, first_name='user_%s' % user_num,
                                 last_name='user_%s' % user_num, num_tel=12345678910, email='user_%s@mail.ru' % user_num)
        Users.objects.get(username='user_0').friends.add(Users.objects.get(username='user_2'))
        group = Groups.objects.create(name='group', slug='group')
        Published.objects.create(name='pub', slug='pub', group=group)

    def test_view_url(self):
        user = Users.objects.get(first_name='user_0')
        resp = self.client.get(reverse('home', kwargs={'user_pk': user.id}))
        self.assertEqual(resp.status_code, 302)

    def test_user_friends(self):
        user = Users.objects.get(first_name='user_0')
        self.assertTrue(user.friends)
        self.assertEqual(user.friends.count(), 1)

    def test_pub_rating(self):
        published = Published.objects.all().select_related('owner').annotate(rat=Avg('rating__star_id'))
        self.assertEqual(published[0].rat, None)


class MessagesViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        for user_num in range(3):
            Users.objects.create(username='user_%s' % user_num, first_name='user_%s' % user_num,
                                 last_name='user_%s' % user_num, num_tel=12345678910,
                                 email='user_%s@mail.ru' % user_num)

    def test_view_url(self):
        user = Users.objects.get(first_name='user_1')
        resp = self.client.get(reverse('messages', kwargs={'user_pk': user.pk}))
        self.assertEqual(resp.status_code, 302)

    def test_chat_members(self):
        users = Users.objects.all()
        chat = Chat.objects.create()
        chat.members.add(users[0], users[1])
        resp = self.client.get(f'/messages/{users[0].pk}/')
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(chat.members.count(), 2)
        self.assertFalse(users[2] in chat.members.all())
        self.assertTrue(users[0] in chat.members.all())


class ChatDetailViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        for user_num in range(3):
            Users.objects.create(username='user_%s' % user_num, first_name='user_%s' % user_num,
                                 last_name='user_%s' % user_num, num_tel=12345678910,
                                 email='user_%s@mail.ru' % user_num)
        chat = [Chat.objects.create() for n in range(2)]
        users = Users.objects.all()
        Message.objects.create(chat=chat[0], author=users[0], message='test1', is_readed=True)
        Message.objects.create(chat=chat[0], author=users[1], message='test2')
        Message.objects.create(chat=chat[0], author=users[0], message='test3')

    def test_view_url(self):
        chat = Chat.objects.get(id=1)
        resp = self.client.get(f'/messages/chat/{chat.id}/')
        self.assertEqual(resp.status_code, 302)

    def test_chat_is_messages(self):
        chat = Chat.objects.all()
        messages = chat[0].message_set.all()
        self.assertTrue(messages)
        self.assertFalse(chat[1].message_set.all())
        self.assertEqual(messages.count(), 3)

    def test_chat_is_readed(self):
        user = Users.objects.get(first_name='user_1')
        chat = Chat.objects.all()
        messages = chat[0].message_set.all()
        self.assertEqual(messages[0].is_readed, True)
        self.assertEqual(messages[1].is_readed == False, messages[2].is_readed == False)
        messages.filter(is_readed=False).exclude(author=user).update(is_readed=True)
        self.assertEqual(messages[1].is_readed == False, messages[2].is_readed == True)


class CreateDialogViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        for user_num in range(3):
            Users.objects.create(username='user_%s' % user_num, first_name='user_%s' % user_num,
                                 last_name='user_%s' % user_num, num_tel=12345678910,
                                 email='user_%s@mail.ru' % user_num)
        chat = [Chat.objects.create() for n in range(2)]
        users = Users.objects.all()
        chat[0].members.add(users[0], users[1])
        chat[1].members.add(users[1], users[2])

    def test_chat(self):
        chat = Chat.objects.all()
        users = Users.objects.all()
        self.assertTrue(users[2] in chat[1].members.all())
        self.assertFalse(users[2] in chat[0].members.all())
        self.assertEqual(users[1] in chat[0].members.all(), users[0] in chat[0].members.all())


class DetailGroupViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        group = Groups.objects.create(name='group_1', slug='group_1')
        Groups.objects.create(name='group_2', slug='group_2')
        for user_num in range(2):
            Users.objects.create(username='user_%s' % user_num, first_name='user_%s' % user_num,
                                 last_name='user_%s' % user_num, num_tel=12345678910,
                                 email='user_%s@mail.ru' % user_num)
        user = Users.objects.get(username='user_1')
        group.users.add(user)
        Published.objects.create(name='pub_1', slug='pub_1', group=group)

    def test_view_url(self):
        group = Groups.objects.get(name='group_1')
        resp = self.client.get(reverse('detail_group', kwargs={'group_slug': group.slug}))
        self.assertEqual(resp.status_code, 302)

    def test_group_and_user(self):
        group = Groups.objects.all()
        users = Users.objects.all()
        self.assertEqual(group[0].users.count() == 1, group[1].users.count() == 0)
        self.assertEqual(users[0].groups_users.count() == 1, users[1].groups_users.count() == 0)

    def test_published_rating(self):
        published = Published.objects.annotate(rat=Avg('rating__star_id')).order_by('-date').get(name='pub_1')
        self.assertEqual(published.rat, None)


class DetailPublishTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        group = Groups.objects.create(name='group_1', slug='group_1')
        Published.objects.create(name='pub_1', slug='pub_1', group=group)

    def test_view_url(self):
        pub = Published.objects.get(name='pub_1')
        resp = self.client.get(reverse('detail_publish', kwargs={'publish_slug': pub.slug}))
        self.assertEqual(resp.status_code, 200)

    def test_published_rating(self):
        published = Published.objects.annotate(rat=Avg('rating__star_id')).order_by('-date').get(name='pub_1')
        self.assertEqual(published.rat, None)
