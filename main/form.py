from django import forms

from main.models import Comments


class AddCommentForm(forms.ModelForm):
    biography = forms.CharField(label='Комментарий',
                                widget=forms.Textarea(attrs={'placeholder': 'Написать комментарий', 'rows': 5}))

    class Meta:
        model = Comments
        fields = ('biography',)
