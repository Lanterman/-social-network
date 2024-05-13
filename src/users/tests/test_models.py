from django.test import TestCase
from django.urls import reverse


from src.users.models import User, Follower, Chat, Message


class UserTest(TestCase):
    """Testing User model"""

    fixtures = ["./config/tests/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user_1 = User.objects.get(id=1)
        cls.user_2 = User.objects.get(id=2)

    def test_num_tel_label(self):
        field_label = self.user_1._meta.get_field('num_tel').verbose_name
        assert field_label == 'mobile number', field_label

    def test_num_tel_max_length(self):
        max_length = self.user_2._meta.get_field('num_tel').max_length
        assert max_length == 20, max_length

    def test_photo_label(self):
        field_label = self.user_1._meta.get_field('photo').upload_to
        assert field_label == 'users/', field_label

    def test_slug_max_length(self):
        max_length = self.user_2._meta.get_field('slug').max_length
        assert max_length == 40, max_length

    def test_str(self):
        expected_object_name = '%s' % self.user_1.username
        assert expected_object_name == str(self.user_1), expected_object_name

    def test_get_absolute_url(self):
        user_URL = self.user_2.get_absolute_url()
        assert user_URL == reverse('home', kwargs={'user_pk': self.user_2.pk}), user_URL


class FollowerTest(TestCase):
    """Testing Follower model"""

    fixtures = ["./config/tests/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.follower_1 = Follower.objects.get(id=1)
        cls.follower_2 = Follower.objects.get(id=2)

    def test_follower_id_label(self):
        field_label = self.follower_1._meta.get_field('follower_id').verbose_name
        assert field_label == 'follower id', field_label
    
    def test_subscription_id_label(self):
        field_label = self.follower_1._meta.get_field('subscription_id').verbose_name
        assert field_label == 'subscription id', field_label

    def test_follower_id_max_length(self):
        max_length = self.follower_2._meta.get_field('follower_id').max_length
        assert max_length == 255, max_length

    def test_is_checked_default_value(self):
        default_value = self.follower_1._meta.get_field('is_checked').default
        assert default_value == False, default_value

    def test_str(self):
        expected_object_name = f'{self.follower_2.follower_id} - {self.follower_2.subscription_id}: {self.follower_2.date}'
        assert expected_object_name == str(self.follower_2), expected_object_name


class ChatTest(TestCase):
    """Testing Chat model"""

    fixtures = ["./config/tests/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = User.objects.get(username='user')
        cls.chat = Chat.objects.get(members=cls.user)

    def test_members_label(self):
        field_label = self.chat._meta.get_field('members').verbose_name
        assert field_label == 'members', field_label

    def test_str(self):
        expected_object_name = f'{self.chat.pk}'
        assert expected_object_name == str(self.chat), str(self.chat)

    def test_get_absolute_url(self):
        chat_URL = reverse('chat', kwargs={'chat_id': self.chat.pk})
        assert self.chat.get_absolute_url() == chat_URL, chat_URL


class MessageTest(TestCase):
    """Testing Message model"""

    fixtures = ["./config/tests/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.message_1 = Message.objects.get(id=1)
        cls.message_2 = Message.objects.get(id=2)

    def test_message_label(self):
        field_label = self.message_1._meta.get_field('message').verbose_name
        assert field_label == 'Message', field_label

    def test_is_readed_label(self):
        field_label = self.message_2._meta.get_field('is_readed').verbose_name
        assert field_label == 'Is read', field_label

    def test_is_readed_default(self):
        field_default = self.message_1._meta.get_field('is_readed').default
        assert field_default == False, field_default

    def test_is_readed(self):
        assert self.message_1.is_readed == True, self.message_1.is_readed 
        assert self.message_2.is_readed == False, self.message_2.is_readed 

    def test_str(self):
        expected_object_name = f'{self.message_2.message}'
        assert expected_object_name == str(self.message_2), expected_object_name
