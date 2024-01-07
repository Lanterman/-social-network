from django.test import TestCase

from src.main.form import *


class AddGroupFormTest(TestCase):
    def test_fields_label(self):
        form = AddGroupForm()
        self.assertTrue(form.fields['name'].label == 'Название')
        self.assertTrue(form.fields['photo'].label == 'Аватарка')


class AddPublishedFormTest(TestCase):
    def test_fields_label(self):
        form = AddPublishedForm()
        self.assertTrue(form.fields['name'].label == 'Название')
        self.assertTrue(form.fields['photo'].label == 'Аватарка')
        self.assertTrue(form.fields['biography'].label == 'Биография')


class RatingFormTest(TestCase):
    def test_fields_label(self):
        form = RatingForm()
        self.assertEqual(form.fields['star'].label, None)
