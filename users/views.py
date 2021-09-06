from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView

from main.views import menu
from users.form import *
from users.models import Users


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        return context

    def form_valid(self, form):
        user = form.save()
        user.slug = user.username
        user.save()
        login(self.request, user)
        return redirect('news')


class ProfileUser(LoginRequiredMixin, DetailView):
    login_url = '/users/login/'
    model = Users
    template_name = 'users/profile.html'
    pk_url_kwarg = 'user_pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Мой профиль'
        return context


def logout_view(request):
    logout(request)
    return redirect('news')


class LoginUser(LoginView):
    template_name = 'users/login.html'
    form_class = LoginUserForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'
        return context


class PasswordChangeUser(PasswordChangeView):
    template_name = 'users/edit_profile.html'
    form_class = PasswordChangeUserForm
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Изменить пароль'
        context['menu'] = menu
        context['button'] = 'Изменить'
        return context


class UpdateUserView(LoginRequiredMixin, UpdateView):
    login_url = '/users/login/'
    model = Users
    form_class = UpdateUserForm
    template_name = 'users/edit_profile.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Изменить профиль'
        context['menu'] = menu
        context['button'] = 'Применить'
        return context
