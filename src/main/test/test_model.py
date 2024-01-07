from django.test import TestCase

from src.main.models import *
from src.users.models import Users


class PublishedTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Объекты, которые используют все методы класса
        group = Groups.objects.create(name='group', slug='group')
        Published.objects.create(name='publish', slug='publish', group_id=group.id, biography='qwe')

    def test_name_label(self):
        published = Published.objects.get(slug='publish')
        field_label = published._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'Название')

    def test_pub_fields(self):
        published = Published.objects.get(slug='publish')
        self.assertEquals(published.group.name, 'group')
        self.assertNotEquals(published.date, 0)

    def test_pub_owner(self):
        published = Published.objects.get(slug='publish')
        self.assertEquals(published.owner_id, None)

    def test_name_max_length(self):
        published = Published.objects.get(slug='publish')
        max_length = published._meta.get_field('name').max_length
        self.assertEquals(max_length, 40)

    def test_name_str(self):
        published = Published.objects.get(slug='publish')
        string = f'{published.name}'
        self.assertEquals(string, str(published))

    def test_get_absolute_url(self):
        published = Published.objects.get(slug='publish')
        self.assertEquals(published.get_absolute_url(), '/publish/publish/')


class GroupsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Объекты, которые используют все методы класса
        user = Users.objects.create(num_tel=123456789101, slug='users')
        Groups.objects.create(name='group_1', slug='group_1', owner_id=user.id)
        Groups.objects.create(name='group_2', slug='group_2')

    def test_owner(self):
        group_1 = Groups.objects.get(slug='group_1')
        group_2 = Groups.objects.get(slug='group_2')
        self.assertTrue(group_1.owner)
        self.assertFalse(group_2.owner)
        self.assertNotEquals(group_1.owner, group_2.owner)

    def test_get_absolute_url(self):
        group = Groups.objects.get(slug='group_1')
        self.assertEquals(group.get_absolute_url(), '/groups/group_1/')


class CommentsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Объекты, которые используют все методы класса
        group = Groups.objects.create(name='group', slug='group')
        user = Users.objects.create(num_tel='123456789101', slug='users')
        published = Published.objects.create(name='publish', slug='publish', group_id=group.id)
        Comments.objects.create(published=published, users=user)

    def test_users_label(self):
        comment = Comments.objects.get(id=1)
        field_label = comment._meta.get_field('users').verbose_name
        self.assertEquals(field_label, 'Пользователь')

    def test_pub_group(self):
        comment = Comments.objects.get(id=1)
        self.assertEquals(comment.users.num_tel, '123456789101')

    def test_name_str(self):
        comment = Comments.objects.get(id=1)
        string = f'{comment.published.name}'
        self.assertEquals(string, str(comment))

    def test_get_absolute_url(self):
        comment = Comments.objects.get(id=1)
        self.assertEquals(comment.get_absolute_url(), '/publish/publish/comments/')


class RatingStarTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Объекты, которые используют все методы класса
        RatingStar.objects.create(value=5)
        RatingStar.objects.create()

    def test_value(self):
        rating_1 = RatingStar.objects.get(value=5)
        field = rating_1._meta.get_field('value').default
        self.assertEquals(rating_1.value, 5)
        self.assertEquals(field, 0)

    def test_name_str(self):
        rating = RatingStar.objects.get(value=5)
        string = f'{rating.value}'
        self.assertEquals(string, str(rating))


class RatingTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Объекты, которые используют все методы класса
        group = Groups.objects.create(name='group', slug='group')
        rating = RatingStar.objects.create(value=5)
        published = Published.objects.create(name='publish', slug='publish', group_id=group.id)
        Rating.objects.create(ip='user', published=published, star=rating)

    def test_fields(self):
        rating = Rating.objects.get(id=1)
        self.assertEquals(rating.star.value, 5)
        self.assertEquals(rating.published.name, 'publish')

    def test_name_str(self):
        rating = Rating.objects.get(id=1)
        string = f'{rating.star} - {rating.published}: {rating.ip}'
        self.assertEquals(string, str(rating))
