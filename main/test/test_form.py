from django.test import TestCase

from main.form import *


class AddCommentFormTest(TestCase):
    def test_biography_field_label(self):
        form = AddCommentForm()
        self.assertTrue(form.fields['biography'].label == 'Комментарий')


class AddGroupFormTest(TestCase):
    def test_fields_label(self):
        form = AddGroupForm()
        self.assertTrue(form.fields['name'].label == 'Название')
        self.assertTrue(form.fields['photo'].label == 'Аватарка')
        self.assertTrue(form.fields['slug'].label == 'URL')


class AddPublishedFormTest(TestCase):
    def test_fields_label(self):
        form = AddPublishedForm()
        self.assertTrue(form.fields['name'].label == 'Название')
        self.assertTrue(form.fields['photo'].label == 'Аватарка')
        self.assertTrue(form.fields['slug'].label == 'URL')
        self.assertTrue(form.fields['biography'].label == 'Биография')


class RatingFormTest(TestCase):
    def test_fields_label(self):
        form = RatingForm()
        self.assertEqual(form.fields['star'].label, None)
