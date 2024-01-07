from django.test import TestCase

from src.users.form import *


class RegisterUserFormTest(TestCase):
    def test_fields_label(self):
        form = RegisterUserForm()
        self.assertTrue(form.fields['username'].label == 'Логин')
        self.assertTrue(form.fields['password1'].label == 'Пароль')
        self.assertTrue(form.fields['password2'].label == 'Повтор пароля')
        self.assertTrue(form.fields['first_name'].label == 'Имя')
        self.assertTrue(form.fields['last_name'].label == 'Фамилия')
        self.assertTrue(form.fields['email'].label == 'Email')
        self.assertTrue(form.fields['num_tel'].label == 'Номер телефона')
        self.assertTrue(form.fields['photo'].label == 'Фото')


class UpdateUserFormTest(TestCase):
    def test_fields_label(self):
        form = UpdateUserForm()
        self.assertTrue(form.fields['first_name'].label == 'Имя')
        self.assertTrue(form.fields['last_name'].label == 'Фамилия')
        self.assertTrue(form.fields['email'].label == 'Email')
        self.assertTrue(form.fields['num_tel'].label == 'Номер телефона')