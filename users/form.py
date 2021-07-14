from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.core.exceptions import ValidationError

from users.models import Users


class AbstractForm(forms.Form):
    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        ab = '!@#$%^&*()_+"№:?-=*<>/\\|][{}1234567890'
        if len(first_name) > 20:
            raise ValidationError('Максимальное число символов 20, у вас %s' % len(first_name))
        if len(first_name) < 3:
            raise ValidationError('Минимальное число символов 3, у вас %s' % len(first_name))
        for n in first_name:
            if n in ab:
                raise ValidationError('Имя должно содержать только буквы')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        ab = '!@#$%^&*()_+"№:?-=*<>/\\|][{}1234567890'
        if len(last_name) > 25:
            raise ValidationError('Максимальное число символов 25, у вас %s' % len(last_name))
        if len(last_name) < 3:
            raise ValidationError('Минимальное число символов 3, у вас %s' % len(last_name))
        for n in last_name:
            if n in ab:
                raise ValidationError('Имя должно содержать только буквы')
        return last_name

    def clean_num_tel(self):
        num_tel = self.cleaned_data['num_tel']
        ab = '1234567890'
        if len(num_tel) < 12:
            raise ValidationError('Минимальное число символов 12, у вас %s' % len(num_tel))
        for n in num_tel:
            if n not in ab:
                raise ValidationError('Номер должен содержать только цифры!')
        return num_tel


class RegisterUserForm(AbstractForm, UserCreationForm):
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


class PasswordChangeUserForm(PasswordChangeForm):
    old_password = forms.CharField(label='Старый пароль', widget=forms.PasswordInput)
    new_password1 = forms.CharField(label='Новый пароль', widget=forms.PasswordInput)
    new_password2 = forms.CharField(label='Подтвердить пароль', widget=forms.PasswordInput)


class UpdateUserForm(AbstractForm):
    first_name = forms.CharField(label='Имя')
    last_name = forms.CharField(label='Фамилия')
    email = forms.EmailField(label='Email', widget=forms.EmailInput)
    num_tel = forms.CharField(max_length=20, label='Номер телефона')
    # def __init__(self, *args, **kwargs):  # Если ModelForm
    #     super().__init__(*args, **kwargs)
    #     self.fields['email'].label = 'Email'
    #     self.fields['email'].required = True
    #     self.fields['first_name'].required = True
    #     self.fields['last_name'].required = True
    #     self.fields['num_tel'].required = True
    #
    # class Meta:
    #     model = Users
    #     fields = ['first_name', 'last_name', 'email', 'num_tel']
