from django.urls import reverse
from django.test import TestCase

from src.users.models import User


class RegisterUserTest(TestCase):
    """Testing RegisterUser endpoint"""

    fixtures = ["./config/tests/test_data.json"]

    def test_view_url(self):
        request = self.client.get(reverse('register'))
        assert request.status_code == 200, request.status_code

    def test_view_template(self):
        request = self.client.get(reverse('register'))
        assert request.status_code == 200, request.status_code
        self.assertTemplateUsed(request, 'users/register.html')

    def test_view_context(self):
        request = self.client.get(reverse('register'))
        assert request.status_code == 200, request.status_code
        assert request.context['title'] == 'Sign-up', request.context['title']
        self.assertTrue('title' in request.context)


class ProfileUserTest(TestCase):
    """Testing ProfileUser endpoint"""

    fixtures = ["./config/tests/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user_1 = User.objects.get(username="admin")
        cls.user_2 = User.objects.get(username="lanterman")

    def test_view_url(self):
        request = self.client.get(reverse('profile', kwargs={'user_pk': self.user_2.pk}))
        assert request.status_code == 302, request.status_code

        request = self.client.get(reverse('profile', kwargs={'user_pk': self.user_2.pk}), follow=True)
        assert request.status_code == 200, request.status_code
        self.assertTemplateUsed(request, 'users/login.html')

        self.client.login(username='lanterman', password='karmavdele')
        with self.assertLogs(level="WARNING"):
            request = self.client.get(reverse('profile', kwargs={'user_pk': self.user_1.pk}))

        request = self.client.get(reverse('profile', kwargs={'user_pk': self.user_2.pk}))
        assert request.status_code == 200, request.status_code
        self.assertTemplateUsed(request, 'users/profile.html')

    def test_view_template(self):
        self.client.login(username='lanterman', password='karmavdele')
        request = self.client.get(reverse('profile', kwargs={'user_pk': self.user_2.pk}))
        assert request.status_code == 200, request.status_code
        assert str(request.context['my_profile']) == 'lanterman', str(request.context['my_profile']) 
        self.assertTemplateUsed(request, 'users/profile.html')

    def test_context_if_not_logged_in(self):
        request = self.client.get(reverse('profile', kwargs={'user_pk': self.user_2.pk}), follow=True)
        self.assertRedirects(request, f'/users/login/?next=/users/profile/{self.user_2.pk}/')
        self.assertTrue('title' in request.context)
        assert request.context['title'] == 'Sign-in', request.context['title']

    def test_context_if_logged_in(self):
        self.client.login(username='lanterman', password='karmavdele')
        request = self.client.get(reverse('profile', kwargs={'user_pk': self.user_2.pk}))
        self.assertTrue('title' in request.context)
        assert request.context['title'] == 'My profile', request.context['title']


class LogoutViewTest(TestCase):
    """Testing the LogoutView endpoint"""

    fixtures = ["./config/tests/test_data.json"]

    def test_view_url(self):
        request = self.client.get(reverse('logout'), follow=True)
        self.assertRedirects(request, '/')

    def test_redirect(self):
        request = self.client.get(reverse('logout'))
        assert request.status_code == 302, request.status_code
        self.assertRedirects(request, '/')


class LoginUserTest(TestCase):
    """Testing the LoginUser endpoint"""

    fixtures = ["./config/tests/test_data.json"]

    def test_view_url(self):
        request = self.client.get(reverse('login'))
        assert request.status_code == 200, request.status_code

    def test_view_template(self):
        request = self.client.get(reverse('login'))
        assert request.status_code == 200, request.status_code
        self.assertTemplateUsed(request, 'users/login.html')

    def test_view_context(self):
        request = self.client.get(reverse('login'))
        assert request.status_code == 200, request.status_code
        assert request.context['title'] == 'Sign-in', request.context['title']
        self.assertTrue('title' in request.context)


class PasswordChangeUserTest(TestCase):
    """Testing the PasswordChangeUser endpoint"""

    fixtures = ["./config/tests/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user_1 = User.objects.get(username='admin')
        cls.user_2 = User.objects.get(username='lanterman')

    def test_view_url(self):
        request = self.client.get(reverse('password_change', kwargs={'slug': self.user_2.slug}))
        assert request.status_code == 302, request.status_code

        request = self.client.get(reverse('password_change', kwargs={'slug': self.user_2.slug}), follow=True)
        assert request.status_code == 200, request.status_code
        self.assertTemplateUsed(request, 'users/login.html')

        self.client.login(username='lanterman', password='karmavdele')
        with self.assertLogs(level="WARNING"):
            request = self.client.get(reverse('password_change', kwargs={'slug': self.user_1.slug}))

        request = self.client.get(reverse('password_change', kwargs={'slug': self.user_2.slug}))
        assert request.status_code == 200, request.status_code
        self.assertTemplateUsed(request, 'users/edit_profile.html')

    def test_view_template(self):
        self.client.login(username='lanterman', password='karmavdele')
        request = self.client.get(reverse('password_change', kwargs={'slug': self.user_2.slug}))
        assert request.status_code == 200, request.status_code
        self.assertTemplateUsed(request, 'users/edit_profile.html')

    def test_view_context(self):
        self.client.login(username='lanterman', password='karmavdele')
        request = self.client.get(reverse('password_change', kwargs={'slug': self.user_2.slug}))
        self.assertTrue('title' in request.context)
        assert request.context['title'] == 'Change password', request.context['title']


class UpdateUserViewTest(TestCase):
    """Testing the UpdateUserView endpoint"""

    fixtures = ["./config/tests/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user_1 = User.objects.get(id=1)
        cls.user_2 = User.objects.get(id=3)

    def test_view_url(self):
        request = self.client.get(reverse('edit_profile', kwargs={'slug': self.user_2.slug}))
        assert request.status_code == 302, request.status_code

        request = self.client.get(reverse('edit_profile', kwargs={'slug': self.user_2.slug}), follow=True)
        assert request.status_code == 200, request.status_code
        self.assertTemplateUsed(request, 'users/login.html')

        self.client.login(username='lanterman', password='karmavdele')
        with self.assertLogs(level="WARNING"):
            request = self.client.get(reverse('edit_profile', kwargs={'slug': self.user_1.slug}))

        request = self.client.get(reverse('edit_profile', kwargs={'slug': self.user_2.slug}))
        assert request.status_code == 200, request.status_code
        self.assertTemplateUsed(request, 'users/edit_profile.html')

    def test_view_template(self):
        self.client.login(username='lanterman', password='karmavdele')
        request = self.client.get(reverse('edit_profile', kwargs={'slug': self.user_2.slug}))
        assert request.status_code == 200, request.status_code
        self.assertTemplateUsed(request, 'users/edit_profile.html')

    def test_view_context(self):
        self.client.login(username='lanterman', password='karmavdele')
        request = self.client.get(reverse('edit_profile', kwargs={'slug': self.user_2.slug}))
        self.assertTrue('title' in request.context)
        assert request.context['title'] == 'Change profile', request.context['title']
