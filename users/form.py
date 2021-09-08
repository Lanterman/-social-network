from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from users.models import Users, Message


class AbstractForm(forms.Form):
    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        ab = '!@#$%^&*()_+"№:?-=*<>/\\|][{}1234567890 '
        if len(first_name) > 20:
            raise ValidationError('Максимальное число символов 20, у вас %s' % len(first_name))
        if len(first_name) < 3 and first_name:
            raise ValidationError('Минимальное число символов 3, у вас %s' % len(first_name))
        for n in first_name:
            if n in ab:
                raise ValidationError('Имя должно содержать только буквы')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        ab = '!@#$%^&*()_+"№:?-=*<>/\\|][{}1234567890 '
        if len(last_name) > 25:
            raise ValidationError('Максимальное число символов 25, у вас %s' % len(last_name))
        if len(last_name) < 3 and last_name:
            raise ValidationError('Минимальное число символов 3, у вас %s' % len(last_name))
        for n in last_name:
            if n in ab:
                raise ValidationError('Имя должно содержать только буквы')
        return last_name

    def clean_num_tel(self):
        num_tel = self.cleaned_data['num_tel']
        ab = '1234567890'
        if len(num_tel) < 12 and num_tel:
            raise ValidationError('Минимальное число символов 12, у вас %s' % len(num_tel))
        for n in num_tel:
            if n not in ab:
                raise ValidationError('Номер должен содержать только цифры!')
        return num_tel

    def clean_email(self):
        email = self.cleaned_data['email']
        if len(email) <= 11:
            raise ValidationError('Email должен содержать более 3 символов перед @!')
        return email


class RegisterUserForm(AbstractForm, UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'placeholder': 'Логин'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'placeholder': 'Повтор пароль'}))
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'placeholder': 'Имя'}))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'placeholder': 'Фамилия'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'placeholder': 'Электронная почта'}))
    num_tel = forms.CharField(label='Номер телефона', widget=forms.TextInput(attrs={'placeholder': 'Номер телефона'}))
    photo = forms.ImageField(label='Фото', required=False)

    class Meta:
        model = Users
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'num_tel', 'photo')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'placeholder': 'Логин'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))


class PasswordChangeUserForm(PasswordChangeForm):
    old_password = forms.CharField(label='Старый пароль',
                                   widget=forms.PasswordInput(attrs={'placeholder': 'Старый пароль'}))
    new_password1 = forms.CharField(label='Новый пароль',
                                    widget=forms.PasswordInput(attrs={'placeholder': 'Новый пароль'}))
    new_password2 = forms.CharField(label='Подтвердить пароль',
                                    widget=forms.PasswordInput(attrs={'placeholder': 'Подтвердить пароль'}))


class UpdateUserForm(AbstractForm, forms.ModelForm):
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'placeholder': 'Имя'}))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'placeholder': 'Фамилия'}))
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    num_tel = forms.CharField(max_length=20, label='Номер телефона',
                              widget=forms.TextInput(attrs={'placeholder': 'Номер телефона'}))

    class Meta:
        model = Users
        fields = ('first_name', 'last_name', 'num_tel', 'email')


class MessageForm(ModelForm):
    message = forms.CharField(label='Сообщения', widget=forms.Textarea(
                                    attrs={'placeholder': 'Написать сообщение', 'rows': 5, 'cols': 90}))

    class Meta:
        model = Message
        fields = ['message']
        labels = {'message': ""}
