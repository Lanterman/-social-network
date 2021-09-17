from django import forms

from main.models import *


class AddCommentForm(forms.ModelForm):
    biography = forms.CharField(label='Комментарий',
                                widget=forms.Textarea(attrs={'placeholder': 'Написать комментарий', 'rows': 5}))

    class Meta:
        model = Comments
        fields = ('biography',)


class AddGroupForm(forms.ModelForm):
    name = forms.CharField(label='Название', widget=forms.TextInput(attrs={'placeholder': 'Имя'}))
    photo = forms.ImageField(label='Аватарка')
    slug = forms.SlugField(label='URL', widget=forms.TextInput(attrs={'placeholder': 'Slug'}))

    class Meta:
        model = Groups
        fields = ('name', 'slug', 'photo')


class AddPublishedForm(forms.ModelForm):
    name = forms.CharField(label='Название', widget=forms.TextInput(attrs={'placeholder': 'Имя'}))
    photo = forms.ImageField(label='Аватарка', required=False)
    slug = forms.SlugField(label='URL', widget=forms.TextInput(attrs={'placeholder': 'Slug'}))
    biography = forms.CharField(label='Биография',
                                widget=forms.Textarea(attrs={'placeholder': 'Написать биографию', 'rows': 5, 'cols': 35}))

    class Meta:
        model = Published
        fields = ('name', 'slug', 'biography', 'photo')


class AddPhotoForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ('photo',)


class RatingForm(forms.ModelForm):
    star = forms.ModelChoiceField(queryset=RatingStar.objects.all(), widget=forms.RadioSelect(), empty_label=None)

    class Meta:
        model = Rating
        fields = ('star',)
