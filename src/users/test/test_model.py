from django.test import TestCase


from src.users.models import *


class UsersTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Users.objects.create(username='user', first_name='user', last_name='user', num_tel=375338632123)

    def test_num_tel_label(self):
        user = Users.objects.get(first_name='user')
        field_label = user._meta.get_field('num_tel').verbose_name
        self.assertEquals(field_label, 'Номер телефона')

    def test_num_tel_max_length(self):
        user = Users.objects.get(first_name='user')
        max_length = user._meta.get_field('num_tel').max_length
        self.assertEquals(max_length, 20)

    def test_photo_label(self):
        user = Users.objects.get(first_name='user')
        field_label = user._meta.get_field('photo').upload_to
        self.assertEquals(field_label, 'users/')

    def test_slug_max_length(self):
        user = Users.objects.get(first_name='user')
        max_length = user._meta.get_field('slug').max_length
        self.assertEquals(max_length, 40)

    def test_str(self):
        user = Users.objects.get(first_name='user')
        expected_object_name = '%s' % user.username
        self.assertEquals(expected_object_name, str(user))

    def test_get_absolute_url(self):
        user = Users.objects.get(first_name='user')
        self.assertEquals(user.get_absolute_url(), reverse('home', kwargs={'user_pk': user.pk}))


class PostSubscribersTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = Users.objects.create(username='user', first_name='user', last_name='user', num_tel=375338632123)
        PostSubscribers.objects.create(owner='user', user=user)

    def test_owner_label(self):
        post = PostSubscribers.objects.get(owner='user')
        field_label = post._meta.get_field('owner').verbose_name
        self.assertEquals(field_label, 'IP')

    def test_owner_max_length(self):
        post = PostSubscribers.objects.get(owner='user')
        max_length = post._meta.get_field('owner').max_length
        self.assertEquals(max_length, 50)

    def test_user_label(self):
        post = PostSubscribers.objects.get(owner='user')
        field_label = post._meta.get_field('user').verbose_name
        self.assertEquals(field_label, 'Пользователь')

    def test_user_max_length(self):
        post = PostSubscribers.objects.get(owner='user')
        max_length = post._meta.get_field('user').max_length
        self.assertEquals(max_length, 50)

    def test_str(self):
        post = PostSubscribers.objects.get(owner='user')
        expected_object_name = f'{post.owner} - {post.user}: {post.date}'
        self.assertEquals(expected_object_name, str(post))


class ChatTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = Users.objects.create(username='user', first_name='user', last_name='user', num_tel=375338632123)
        chat = Chat.objects.create()
        chat.members.add(user)

    def test_members_label(self):
        user = Users.objects.get(first_name='user')
        chat = Chat.objects.get(members=user)
        field_label = chat._meta.get_field('members').verbose_name
        self.assertEquals(field_label, 'Участник')

    def test_str(self):
        user = Users.objects.get(first_name='user')
        chat = Chat.objects.get(members=user)
        expected_object_name = f'{chat.pk}'
        self.assertEquals(expected_object_name, str(chat))

    def test_get_absolute_url(self):
        user = Users.objects.get(first_name='user')
        chat = Chat.objects.get(members=user)
        self.assertEquals(chat.get_absolute_url(), reverse('chat', kwargs={'chat_id': chat.pk}))


class MessageTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = Users.objects.create(username='user', first_name='user', last_name='user', num_tel=375338632123)
        chat = Chat.objects.create()
        chat.members.add(user)
        Message.objects.create(chat=chat, author=user, message='test_1', is_readed=True)
        Message.objects.create(chat=chat, author=user, message='test_2')

    def test_message_label(self):
        message = Message.objects.get(message='test_1')
        field_label = message._meta.get_field('message').verbose_name
        self.assertEquals(field_label, 'Сообщение')

    def test_is_readed_label(self):
        message = Message.objects.get(message='test_1')
        field_label = message._meta.get_field('is_readed').verbose_name
        self.assertEquals(field_label, 'Прочитано')

    def test_is_readed_default(self):
        message = Message.objects.get(message='test_1')
        field_default = message._meta.get_field('is_readed').default
        self.assertEquals(field_default, False)

    def test_is_readed(self):
        message_1 = Message.objects.get(message='test_1')
        message_2 = Message.objects.get(message='test_2')
        self.assertEquals(message_1.is_readed, True)
        self.assertEquals(message_2.is_readed, False)

    def test_str(self):
        message = Message.objects.get(message='test_1')
        expected_object_name = f'{message.message}'
        self.assertEquals(expected_object_name, str(message))
