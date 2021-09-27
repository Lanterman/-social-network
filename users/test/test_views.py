from django.test import TestCase

from users.models import *
from django.urls import reverse


class RegisterUserTest(TestCase):

    def test_view_url(self):
        resp = self.client.get(reverse('register'))
        self.assertEqual(resp.status_code, 200)

    def test_view_template(self):
        resp = self.client.get(reverse('register'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'users/register.html')

    def test_view_context(self):
        resp = self.client.get(reverse('register'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('title' in resp.context)
        self.assertEqual(resp.context['title'], 'Регистрация')


class ProfileUserTest(TestCase):

    def setUp(self):
        Users.objects.create_user(username='testuser1', password='12345', first_name='user1', last_name='user1',
                                  num_tel=12345678910, email='test1@mail.ru', slug='user1')

    def test_view_url(self):
        user = Users.objects.get(username='testuser1')
        resp = self.client.get(reverse('profile', kwargs={'user_pk': user.pk}), follow=True)
        self.assertEqual(resp.status_code, 200)

    def test_view_template(self):
        self.client.login(username='testuser1', password='12345')
        user = Users.objects.get(username='testuser1')
        resp = self.client.get(reverse('profile', kwargs={'user_pk': user.pk}))
        # Проверка что пользователь залогинился
        self.assertEqual(str(resp.context['user']), 'testuser1')
        self.assertTemplateUsed(resp, 'users/profile.html')

    def test_context_if_not_logged_in(self):
        user = Users.objects.get(username='testuser1')
        resp = self.client.get(reverse('profile', kwargs={'user_pk': user.pk}), follow=True)
        self.assertRedirects(resp, f'/users/login/?next=/users/profile/{user.pk}/')
        self.assertTrue('title' in resp.context)
        self.assertEqual(resp.context['title'], 'Авторизация')

    def test_context_if_logged_in(self):
        self.client.login(username='testuser1', password='12345')
        user = Users.objects.get(username='testuser1')
        resp = self.client.get(reverse('profile', kwargs={'user_pk': user.pk}))
        self.assertTrue('title' in resp.context)
        self.assertEqual(resp.context['title'], 'Мой профиль')


class LogoutViewTest(TestCase):

    def test_view_url(self):
        resp = self.client.get(reverse('logout'), follow=True)
        self.assertRedirects(resp, '/')

    def test_redirect(self):
        resp = self.client.get(reverse('logout'))
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, '/')


class LoginUserTest(TestCase):

    def test_view_url(self):
        resp = self.client.get(reverse('login'))
        self.assertEqual(resp.status_code, 200)

    def test_view_template(self):
        resp = self.client.get(reverse('login'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'users/login.html')

    def test_view_context(self):
        resp = self.client.get(reverse('login'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('title' in resp.context)
        self.assertEqual(resp.context['title'], 'Авторизация')


class PasswordChangeUserTest(TestCase):

    def setUp(self):
        Users.objects.create_user(username='testuser1', password='12345', first_name='user1', last_name='user1',
                                  num_tel=12345678910, email='test1@mail.ru', slug='user1')

    def test_view_url(self):
        user = Users.objects.get(username='testuser1')
        resp = self.client.get(reverse('password_change', kwargs={'slug': user.slug}))
        self.assertEqual(resp.status_code, 302)

    def test_view_template(self):
        self.client.login(username='testuser1', password='12345')
        user = Users.objects.get(username='testuser1')
        resp = self.client.get(reverse('password_change', kwargs={'slug': user.slug}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'users/edit_profile.html')

    def test_view_context(self):
        self.client.login(username='testuser1', password='12345')
        user = Users.objects.get(username='testuser1')
        resp = self.client.get(reverse('password_change', kwargs={'slug': user.slug}))
        self.assertTrue('title' in resp.context)
        self.assertEqual(resp.context['title'], 'Изменить пароль')


class UpdateUserViewTest(TestCase):

    def setUp(self):
        Users.objects.create_user(username='testuser1', password='12345', first_name='user1', last_name='user1',
                                  num_tel=12345678910, email='test1@mail.ru', slug='user1')

    def test_view_url(self):
        user = Users.objects.get(username='testuser1')
        resp = self.client.get(reverse('edit_profile', kwargs={'slug': user.slug}))
        self.assertEqual(resp.status_code, 302)

    def test_view_template(self):
        self.client.login(username='testuser1', password='12345')
        user = Users.objects.get(username='testuser1')
        resp = self.client.get(reverse('edit_profile', kwargs={'slug': user.slug}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'users/edit_profile.html')

    def test_view_context(self):
        self.client.login(username='testuser1', password='12345')
        user = Users.objects.get(username='testuser1')
        resp = self.client.get(reverse('edit_profile', kwargs={'slug': user.slug}))
        self.assertTrue('title' in resp.context)
        self.assertEqual(resp.context['title'], 'Изменить профиль')
