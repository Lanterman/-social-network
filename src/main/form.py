import re

from django import forms
from django.core.exceptions import ValidationError

from src.main.models import *
from src.users.models import Users


class AbstractForm(forms.ModelForm):
    def clean_name(self):
        name = self.cleaned_data['name']
        re_value = re.findall(r'[^\w ]', name)
        if re_value:
            raise ValidationError(f"Имя не может содержать данные символ(-ы): {', '.join(re_value)}")
        return name


class AddGroupForm(AbstractForm):
    name = forms.CharField(label='Название', widget=forms.TextInput(attrs={'placeholder': 'Имя'}))
    photo = forms.ImageField(label='Аватарка')

    class Meta:
        model = Groups
        fields = ('name', 'photo')


class AddPublishedForm(AbstractForm):
    name = forms.CharField(label='Название', widget=forms.TextInput(attrs={'placeholder': 'Имя'}))
    photo = forms.ImageField(label='Аватарка', required=False)
    biography = forms.CharField(label='Биография',
                                widget=forms.Textarea(attrs={'placeholder': 'Написать биографию', 'rows': 5, 'cols': 35}))

    class Meta:
        model = Published
        fields = ('name', 'biography', 'photo')


class AddPhotoForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ('photo',)


class RatingForm(forms.ModelForm):
    star = forms.ModelChoiceField(queryset=RatingStar.objects.all(), widget=forms.RadioSelect(), empty_label=None)

    class Meta:
        model = Rating
        fields = ('star',)
