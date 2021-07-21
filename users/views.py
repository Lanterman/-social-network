from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

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


@login_required(login_url='/users/login/')
def profile(request, user_slug):
    user1 = Users.objects.get(username=user_slug)
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
    form_class = LoginUserForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'
        return context


class PasswordChangeUser(PasswordChangeView):
    template_name = 'users/password_change.html'
    form_class = PasswordChangeUserForm
    success_url = reverse_lazy('news')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Изменить пароль'
        context['menu'] = menu
        return context


@login_required
def update(request, slug):
    us = Users.objects.get(slug=slug)
    form = UpdateUserForm()
    if request.method == 'POST':
        form = UpdateUserForm(request.POST)
        if form.is_valid():
            us.first_name = request.POST['first_name']
            us.last_name = request.POST['last_name']
            us.email = request.POST['email']
            us.num_tel = request.POST['num_tel']
            us.save()
            return redirect('news')
    context = {'title': 'Изменить профиль', 'form': form, 'menu': menu}
    return render(request, 'users/edit_profile.html', context)
