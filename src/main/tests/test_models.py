from django.urls import reverse
from django.test import TestCase

from src.main.models import Publication, Group, Comment, RatingStar, Rating


class PublicationTest(TestCase):
    """Testing the Publication model"""

    fixtures = ["./config/tests/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.publication = Publication.objects.get(id=1)

    def test_name_label(self):
        field_label = self.publication._meta.get_field('name').verbose_name
        assert field_label == 'name', field_label

    def test_name_max_length(self):
        max_length = self.publication._meta.get_field('name').max_length
        assert max_length == 40, max_length

    def test_photo_label(self):
        field_label = self.publication._meta.get_field('photo').upload_to
        assert field_label == 'publication/', field_label

    def test_slug_max_length(self):
        max_length = self.publication._meta.get_field('slug').max_length
        assert max_length == 40, max_length

    def test_str(self):
        assert self.publication.__str__() == self.publication.name, self.publication.__str__()

    def test_get_absolute_url(self):
        publication_URL = f'/publish/{self.publication.slug}/'
        assert publication_URL == self.publication.get_absolute_url(), publication_URL


class GroupTest(TestCase):
    """Testing the Group model"""

    fixtures = ["./config/tests/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.group = Group.objects.get(id=1)

    def test_name_label(self):
        field_label = self.group._meta.get_field('name').verbose_name
        assert field_label == 'name', field_label

    def test_name_max_length(self):
        max_length = self.group._meta.get_field('name').max_length
        assert max_length == 40, max_length

    def test_photo_label(self):
        field_label = self.group._meta.get_field('photo').upload_to
        assert field_label == 'groups/', field_label

    def test_slug_max_length(self):
        max_length = self.group._meta.get_field('slug').max_length
        assert max_length == 40, max_length

    def test_str(self):
        assert self.group.__str__() == self.group.name, self.group.__str__()

    def test_get_absolute_url(self):
        group_URL = f'/groups/{self.group.slug}/'
        assert group_URL == self.group.get_absolute_url(), group_URL


class CommentTest(TestCase):
    """Testing the Comment model"""

    fixtures = ["./config/tests/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.publication = Publication.objects.get(id=1)
        cls.comment = Comment.objects.get(id=1)

    def test_date_label(self):
        field_label = self.comment._meta.get_field('date').verbose_name
        assert field_label == 'date', field_label

    def test_biography_label(self):
        field_label = self.comment._meta.get_field('biography').verbose_name
        assert field_label == 'biography', field_label

    def test_str(self):
        assert self.comment.__str__() == self.publication.name, self.comment.__str__()

    def test_get_absolute_url(self):
        group_URL = f'/publish/{self.publication.slug}/comments/'
        assert group_URL == self.comment.get_absolute_url(), group_URL


class RatingStarTest(TestCase):
    """Testing the RatingStar model"""

    fixtures = ["./config/tests/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.rating_star = RatingStar.objects.get(id=3)

    def test_value_label(self):
        field_label = self.rating_star._meta.get_field('value').verbose_name
        assert field_label == 'rating', field_label
    
    def test_default_value_of_value_label(self):
        default_value = self.rating_star._meta.get_field('value').default
        assert default_value == 0, default_value        

    def test_str(self):
        assert self.rating_star.__str__() == f"{self.rating_star.value}", self.rating_star.__str__()

class RatingTest(TestCase):
    """Testing the Rating model"""

    fixtures = ["./config/tests/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.publication = Publication.objects.get(id=1)
        cls.rating = Rating.objects.create(ip="lanterman", publication_id_id=1, star_id=1)

    def test_ip_label(self):
        field_label = self.rating._meta.get_field('ip').verbose_name
        assert field_label == 'IP', field_label
    
    def test_ip_max_length(self):
        max_length = self.rating._meta.get_field('ip').max_length
        assert max_length == 150, max_length

    def test_str(self):
        string = f'{self.rating.star} - {self.publication.name}: {self.rating.ip}'
        assert self.rating.__str__() == string, self.rating.__str__()

