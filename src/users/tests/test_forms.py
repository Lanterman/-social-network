from django.test import TestCase
from django.core.exceptions import ValidationError

from src.users.models import User
from src.users.form import AbstractForm, RegisterUserForm, PasswordChangeUserForm, UpdateUserForm


class AbstractFormTest(TestCase):
    """Testing the AbstractForm class methods"""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.instance = AbstractForm()
    
    def test_clean_first_name(self):
        "Testing the clean_first_name method"

        # Error: More than 20 characters
        self.instance.cleaned_data = {"first_name": "first_name_more_twenty_letters"}
        with self.assertRaisesMessage(ValidationError, "The maximum number of characters is 20, you have 30"):
            self.instance.clean_first_name()
        
        # Error: Less than 3 characters
        self.instance.cleaned_data = {"first_name": "as"}
        with self.assertRaisesMessage(ValidationError, "The minimum number of characters is 3, you have 2"):
            self.instance.clean_first_name()
        
        # Error: Contain only letters
        self.instance.cleaned_data = {"first_name": "first!name"}
        with self.assertRaisesMessage(ValidationError, "The first name must contain only letters!"):
            self.instance.clean_first_name()
        
        # Correct
        self.instance.cleaned_data = {"first_name": "first_name"}
        form = self.instance.clean_first_name()
        assert form == "first_name", form
    
    def test_clean_last_name(self):
        "Testing the clean_last_name method"

        # Error: More than 25 characters
        self.instance.cleaned_data = {"last_name": "last_name_more_twenty_five_letters"}
        with self.assertRaisesMessage(ValidationError, "The maximum number of characters is 25, you have 34"):
            self.instance.clean_last_name()
        
        # Error: Less than 3 characters
        self.instance.cleaned_data = {"last_name": "as"}
        with self.assertRaisesMessage(ValidationError, "The minimum number of characters is 3, you have 2"):
            self.instance.clean_last_name()
        
        # Error: Contain only letters
        self.instance.cleaned_data = {"last_name": "last!name"}
        with self.assertRaisesMessage(ValidationError, "The last name must contain only letters!"):
            self.instance.clean_last_name()
        
        # Correct
        self.instance.cleaned_data = {"last_name": "last_name"}
        form = self.instance.clean_last_name()
        assert form == "last_name", form
    
    def test_clean_num_tel(self):
        "Testing the clean_num_tel method"

        # Error: More than 20 characters
        self.instance.cleaned_data = {"num_tel": "123123123123123123123123"}
        with self.assertRaisesMessage(ValidationError, "The maximum number of characters is 20, you have 24"):
            self.instance.clean_num_tel()
        
        # Error: Less than 12 characters
        self.instance.cleaned_data = {"num_tel": "1212121212"}
        with self.assertRaisesMessage(ValidationError, "The minimum number of characters is 12, you have 10"):
            self.instance.clean_num_tel()
        
        # Error: Contain only numbers
        self.instance.cleaned_data = {"num_tel": "1212121212q"}
        with self.assertRaisesMessage(ValidationError, "The number must contain only numbers!"):
            self.instance.clean_num_tel()
        
        # Correct
        self.instance.cleaned_data = {"num_tel": "21123123123123123"}
        form = self.instance.clean_num_tel()
        assert form == "21123123123123123", form
    
    def test_clean_email(self):
        "Testing the clean_email method"

        # Error: Less than 3 characters before @
        self.instance.cleaned_data = {"email": "q@mail.ru"}
        with self.assertRaisesMessage(ValidationError, "Email must contain more than 3 characters before @!"):
            self.instance.clean_email()
        
        # Correct
        self.instance.cleaned_data = {"email": "mail@mail.ru"}
        form = self.instance.clean_email()
        assert form == "mail@mail.ru", form


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


class PasswordChangeUserFormTest(TestCase):
    """Testing the PasswordChangeUserForm class methods"""

    fixtures = ["./config/tests/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = User.objects.get(id=1)
        cls.instance = PasswordChangeUserForm(cls.user)
    
    def test_clean_new_password1(self):
        """Testing the clean_new_password1 method"""

        # Error: same passswords
        self.instance.cleaned_data = {"old_password": "old_password", "new_password1": "old_password"}
        with self.assertRaisesMessage(ValidationError, "Old and new passwords should not be the same!"):
            self.instance.clean_new_password1()
        
        # Correct
        self.instance.cleaned_data = {"old_password": "old_password", "new_password1": "new_password1"}
        form = self.instance.clean_new_password1()
        assert form == "new_password1", form


class UpdateUserFormTest(TestCase):
    def test_fields_label(self):
        form = UpdateUserForm()
        assert form.fields['first_name'].label == 'First name', form.fields['first_name'].label
        assert form.fields['last_name'].label == 'Last name', form.fields['last_name'].label
        assert form.fields['email'].label == 'Email', form.fields['email'].label
        assert form.fields['num_tel'].label == 'Mobile number', form.fields['num_tel'].label