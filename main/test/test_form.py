from django.test import TestCase

from main.form import *


class AddCommentFormTest(TestCase):
    def test_biography_field_label(self):
        form = AddCommentForm()
        self.assertTrue(form.fields['biography'].label == 'Комментарий')
