from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from users.models import Users


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput)
    first_name = forms.CharField(label='Имя', required=False)
    last_name = forms.CharField(label='Фамилия', required=False)
    email = forms.EmailField(label='Email', required=False, widget=forms.EmailInput)
    num_tel = forms.CharField(label='Номер телефона', required=False)
    photo = forms.ImageField(label='Фото', required=False)

    class Meta:
        model = Users
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'num_tel', 'photo')
