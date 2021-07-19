from django import forms

from main.models import Comments


# class CommentsUserForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['biography'].label = 'Оставить отзыв'
#         self.fields['biography'].widget = forms.TextInput()
#
#     class Meta:
#         model = Comments
#         fields = ('biography', 'published', 'users')


class AddCommentForm(forms.ModelForm):
    biography = forms.CharField(label='Комментарий',
                                widget=forms.Textarea(attrs={'placeholder': 'Написать комментарий', 'rows': 5}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['users'].empty_label = 'Выберите пользователя'
        self.fields['users'].label = 'Пользователь'
        self.fields['published'].label = 'Публикация'
        self.fields['published'].empty_label = 'Выберите публикацию'

    class Meta:
        model = Comments
        fields = ('biography', 'users', 'published')
