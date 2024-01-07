from django.contrib.auth.mixins import LoginRequiredMixin


menu = [
    {'name': 'Главная страница', 'url': 'home'},
    {'name': 'Сообщения', 'url': 'messages'},
    {'name': 'Друзья', 'url': 'friends'},
    {'name': 'Группы', 'url': 'groups'}
]


class DataMixin(LoginRequiredMixin):
    login_url = '/users/login/'

    def get_context(self, **kwargs):
        context = kwargs
        context['menu'] = menu
        return context
