from django.test import TestCase

from src.users.form import *


class RegisterUserFormTest(TestCase):
    def test_fields_label(self):
        form = RegisterUserForm()
        assert form.fields['username'].label == 'Username', form.fields['username'].label
        assert form.fields['password1'].label == 'Password', form.fields['password1'].label
        assert form.fields['password2'].label == 'Confirm password', form.fields['password2'].label
        assert form.fields['first_name'].label == 'First name', form.fields['first_name'].label
        assert form.fields['last_name'].label == 'Last name', form.fields['last_name'].label
        assert form.fields['email'].label == 'Email', form.fields['email'].label
        assert form.fields['num_tel'].label == 'Mobile number', form.fields['num_tel'].label
        assert form.fields['photo'].label == 'Photo', form.fields['photo'].label


class UpdateUserFormTest(TestCase):
    def test_fields_label(self):
        form = UpdateUserForm()
        assert form.fields['first_name'].label == 'First name', form.fields['first_name'].label
        assert form.fields['last_name'].label == 'Last name', form.fields['last_name'].label
        assert form.fields['email'].label == 'Email', form.fields['email'].label
        assert form.fields['num_tel'].label == 'Mobile number', form.fields['num_tel'].label