import re

from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, AuthenticationForm
from django.core.exceptions import ValidationError

from src.users.models import User


class AbstractForm(forms.Form):
    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        re_value = re.findall(r'\d|\W', first_name)
        invalid_list = []
        if len(first_name) > 20:
            invalid_list.append(ValidationError('Максимальное число символов 20, у вас %(value)s',
                                                params={'value': len(first_name)}))
        if len(first_name) < 3 and first_name:
            invalid_list.append(ValidationError('Минимальное число символов 3, у вас %(value)s',
                                                params={'value': len(first_name)}))
        if re_value:
            invalid_list.append(ValidationError('Имя должно содержать только буквы'))
        if invalid_list:
            raise ValidationError(invalid_list)
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        re_value = re.findall(r'\d|\W', last_name)
        invalid_list = []
        if len(last_name) > 25:
            invalid_list.append(ValidationError('Максимальное число символов 25, у вас %(value)s',
                                                params={'value': len(last_name)}))
        if len(last_name) < 3 and last_name:
            invalid_list.append(ValidationError('Минимальное число символов 3, у вас %(value)s',
                                                params={'value': len(last_name)}))
        if re_value:
            invalid_list.append(ValidationError('Имя должно содержать только буквы'))
        if invalid_list:
            raise ValidationError(invalid_list)
        return last_name

    def clean_num_tel(self):
        num_tel = self.cleaned_data['num_tel']
        re_value = re.findall(r'\D', num_tel)
        invalid_list = []
        if len(num_tel) < 12 and num_tel:
            invalid_list.append(ValidationError('Минимальное число символов 12, у вас %(value)s',
                                                params={'value': len(num_tel)}))
        if len(num_tel) > 20 and num_tel:
            invalid_list.append(ValidationError('Максимальное число символов 20, у вас %(value)s',
                                                params={'value': len(num_tel)}))
        if re_value:
            invalid_list.append(ValidationError('Номер должен содержать только цифры!'))
        if invalid_list:
            raise ValidationError(invalid_list)
        return num_tel

    def clean_email(self):
        email = self.cleaned_data['email']
        if len(email) <= 11:
            raise ValidationError('Email должен содержать более 3 символов перед @!')
        return email


class RegisterUserForm(AbstractForm, UserCreationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}))
    first_name = forms.CharField(label='First name', widget=forms.TextInput(attrs={'placeholder': 'First name'}))
    last_name = forms.CharField(label='Last name', widget=forms.TextInput(attrs={'placeholder': 'Last name'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    num_tel = forms.CharField(label='Mobile number', widget=forms.TextInput(attrs={'placeholder': 'Mobile number'}))
    photo = forms.ImageField(label='Photo', required=False)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'num_tel', 'photo')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


class PasswordChangeUserForm(PasswordChangeForm):
    old_password = forms.CharField(label='Old password',
                                   widget=forms.PasswordInput(attrs={'placeholder': 'Old password'}))
    new_password1 = forms.CharField(label='New password',
                                    widget=forms.PasswordInput(attrs={'placeholder': 'New password'}))
    new_password2 = forms.CharField(label='Confrim password',
                                    widget=forms.PasswordInput(attrs={'placeholder': 'Confrim password'}))
    
    def clean_new_password1(self):
        old_password = self.cleaned_data.get('old_password')
        new_password1 = self.cleaned_data.get('new_password1')

        if old_password == new_password1:
            raise ValidationError('Old and new passwords should not be the same!')
        return new_password1


class UpdateUserForm(AbstractForm, forms.ModelForm):
    first_name = forms.CharField(label='First name', widget=forms.TextInput(attrs={'placeholder': 'First name'}))
    last_name = forms.CharField(label='Last name', widget=forms.TextInput(attrs={'placeholder': 'Last name'}))
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    num_tel = forms.CharField(max_length=20, label='Mobile number', 
                              widget=forms.TextInput(attrs={'placeholder': 'Mobile number'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'num_tel', 'email')
