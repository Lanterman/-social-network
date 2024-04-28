from django.test import TestCase
from django.core.exceptions import ValidationError

from src.main.form import AddGroupForm, AddPublishedForm, RatingForm


class AddGroupFormTest(TestCase):
    """Testing the AddGroupForm form"""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.instance = AddGroupForm()
    
    def test_fields_label(self):
        assert self.instance.fields['name'].label == 'Name', self.instance.fields['name']
        assert self.instance.fields['photo'].label == 'Photo', self.instance.fields['photo']
    
    def test_clean_name(self):
        "Testing the clean_name method"

        self.instance.cleaned_data = {"name": "my first!name1@"}
        with self.assertRaisesMessage(ValidationError, "Name can not these characters: !, @"):
            self.instance.clean_name()

        self.instance.cleaned_data = {"name": "my first name_1"}
        form = self.instance.clean_name()
        assert form == "my first name_1", form


class AddPublishedFormTest(TestCase):
    """Testing the AddPublishedForm form"""

    def test_fields_label(self):
        form = AddPublishedForm()
        assert form.fields['name'].label == 'Name', form.fields['name']
        assert form.fields['photo'].label == 'Photo', form.fields['photo']
        assert form.fields['biography'].label == 'Biography', form.fields['biography']


class RatingFormTest(TestCase):
    """Testing the RatingForm form"""

    def test_fields_label(self):
        form = RatingForm()
        self.assertEqual(form.fields['star'].label, None)
