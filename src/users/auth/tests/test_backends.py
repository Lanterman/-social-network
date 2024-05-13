from django.urls import reverse
from django.test import TestCase
from django.test.client import RequestFactory

from src.users.auth import backends
from src.users.models import User


class TestCustomAuthBackend(TestCase):
    """Testing the CustomAuthBackend class"""

    fixtures = ["./config/tests/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.admin = User.objects.get(id=1)
        cls.user = User.objects.get(id=3)

        cls.request = RequestFactory()
        cls.url = reverse("profile", kwargs={"user_pk": cls.user.id})

        cls.instance = backends.CustomAuthBackend()

    def test_invalid_authenticate_by_not_username(self):
        """Testing invalid authentiacte by have not the username"""

        request = self.request.get(self.url)
        response = self.instance.authenticate(request, password="karmavdele")
        assert response == None, response
    
    def test_invalid_authenticate_by_username_is_none(self):
        """Testing invalid authentiacte by the username is None"""

        request = self.request.get(self.url)
        response = self.instance.authenticate(request, password="karmavdele", username=None)
        assert response == None, response
    
    def test_invalid_authenticate_by_not_password(self):
        """Testing invalid authentiacte by have not the password"""

        request = self.request.get(self.url)
        response = self.instance.authenticate(request, username=self.user.username)
        assert response == None, response
    
    def test_invalid_authenticate_by_password_is_none(self):
        """Testing invalid authentiacte by the password is None"""

        request = self.request.get(self.url)
        response = self.instance.authenticate(request, username=self.user.username, password=None)
        assert response == None, response
    
    def test_invalid_authenticate_by_user_does_not_exist(self):
        """Testing valid authenticate by the user doesn't exist"""

        request = self.request.get(self.url)
        response = self.instance.authenticate(request, "self.user.username", "karmavdele")
        assert response == None, response
    
    def test_valid_authenticate_by_user_is_staff(self):
        """Testing valid authenticate by the user is staff"""

        request = self.request.get(self.url)
        response = self.instance.authenticate(request, self.admin.username, "admin")
        assert response == self.admin, response
        assert response.username == self.admin.username, response
    
    def test_invalid_authenticate_by_password_is_wrong(self):
        """Testing valid authenticate by the password is wrong"""

        request = self.request.get(self.url)
        response = self.instance.authenticate(request, self.user.username, "karmavdele1")
        assert response == None, response
    
    def test_valid_authenticate(self):
        """Testing valid authenticate"""

        request = self.request.get(self.url)
        response = self.instance.authenticate(request, self.user.username, "karmavdele")
        assert response == self.user, response
        assert response.username == self.user.username, response
