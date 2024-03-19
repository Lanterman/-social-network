import re

from django import forms
from django.core.exceptions import ValidationError

from src.main.models import Publication, Group, Rating, RatingStar
from src.users.models import User


class AbstractForm(forms.ModelForm):
    def clean_name(self):
        name = self.cleaned_data['name']
        re_value = re.findall(r'[^\w ]', name)
        if re_value:
            raise ValidationError(f"Name can not these characters: {', '.join(re_value)}")
        return name


class AddGroupForm(AbstractForm):
    name = forms.CharField(label='Name', widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    photo = forms.ImageField(label='Photo')

    class Meta:
        model = Group
        fields = ('name', 'photo')


class AddPublishedForm(AbstractForm):
    name = forms.CharField(label='Name', widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    photo = forms.ImageField(label='Photo', required=False, localize=True)
    biography = forms.CharField(label='Biography',
                                widget=forms.Textarea(attrs={'placeholder': 'Write biography', 'rows': 5, 'cols': 35}))

    class Meta:
        model = Publication
        fields = ('name', 'biography', 'photo')


class AddPhotoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('photo',)


class RatingForm(forms.ModelForm):
    star = forms.ModelChoiceField(queryset=RatingStar.objects.all(), widget=forms.RadioSelect(), empty_label=None)

    class Meta:
        model = Rating
        fields = ('star',)
