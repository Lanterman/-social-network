from django.test import TestCase

from src.main.form import *


class AddGroupFormTest(TestCase):
    def test_fields_label(self):
        form = AddGroupForm()
        assert form.fields['name'].label == 'Name', form.fields['name']
        assert form.fields['photo'].label == 'Photo', form.fields['photo']


class AddPublishedFormTest(TestCase):
    def test_fields_label(self):
        form = AddPublishedForm()
        assert form.fields['name'].label == 'Name', form.fields['name']
        assert form.fields['photo'].label == 'Photo', form.fields['photo']
        assert form.fields['biography'].label == 'Biography', form.fields['biography']


class RatingFormTest(TestCase):
    def test_fields_label(self):
        form = RatingForm()
        self.assertEqual(form.fields['star'].label, None)
