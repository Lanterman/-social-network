from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView

from src.main.utils import DataMixin, menu
from src.users import tasks
from src.users.form import LoginUserForm, PasswordChangeUserForm, RegisterUserForm, UpdateUserForm
from src.users.models import User


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Sign-up'
        return context

    def form_valid(self, form):
        user = form.save()
        user.slug = user.username
        user.save()
        login(self.request, user)
        # tasks.send_registration_message.delay(user.email)
        return redirect('news')


class ProfileUser(DataMixin, DetailView):
    model = User
    template_name = 'users/profile.html'
    pk_url_kwarg = 'user_pk'
    context_object_name = "my_profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context | self.get_context(title='My profile')


def logout_view(request):
    logout(request)
    return redirect('news')


class LoginUser(LoginView):
    template_name = 'users/login.html'
    form_class = LoginUserForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Sign-in'
        return context


class PasswordChangeUser(PasswordChangeView, DetailView):
    model = User
    slug_url_kwarg = 'slug'
    template_name = 'users/edit_profile.html'
    form_class = PasswordChangeUserForm
    success_url = reverse_lazy('news')
    context_object_name = "my_profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Change password'
        context['menu'] = menu
        context['button'] = 'Submit'
        return context
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.get(self, request, *args, **kwargs)


class UpdateUserView(DataMixin, UpdateView):
    model = User
    form_class = UpdateUserForm
    template_name = 'users/edit_profile.html'
    slug_url_kwarg = 'slug'
    context_object_name = "my_profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context | self.get_context(title='Change profile', button='Submit')
