from django import forms

from main.models import Comments


class CommentsUserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['biography'].label = 'Оставить отзыв'
        self.fields['biography'].widget = forms.TextInput()

    class Meta:
        model = Comments
        fields = ('biography', 'published', 'users')
