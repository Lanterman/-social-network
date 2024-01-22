from django.contrib.auth.mixins import LoginRequiredMixin


menu = [
    {'name': 'Home', 'url': 'home'},
    {'name': 'Messengers', 'url': 'messages'},
    {'name': 'Followers', 'url': 'followers'},
    # {'name': 'Subscriptions', 'url': 'subscriptions'},
    {'name': 'Groups', 'url': 'groups'}
]


class DataMixin(LoginRequiredMixin):
    login_url = '/users/login/'

    def get_context(self, **kwargs):
        context = kwargs
        context['menu'] = menu
        return context
