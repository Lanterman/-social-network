from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.views.generic import CreateView, DetailView

from main.views import menu
from users.form import *


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        context['menu'] = menu
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('news')


def profile(request, username):
    user1 = Users.objects.get(username=username)
    context = {'title': 'Мой профиль', 'menu': menu, 'user1': user1}
    return render(request, 'users/profile.html', context)


# class ProfileUser(LoginRequiredMixin, DetailView):
#     login_url = '/users/login/'
#     model = Users
#     template_name = 'users/profile.html'
#     slug_url_kwarg = 'username'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['menu'] = menu
#         context['title'] = 'Мой профиль'


def logout_view(request):
    logout(request)
    return redirect('news')


class LoginUser(LoginView):
    template_name = 'users/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'
        return context
