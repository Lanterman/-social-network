from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView
from django.core.exceptions import PermissionDenied

from config import settings
from src.main.utils import DataMixin, menu
from . import tasks, services, db_queries
from .form import LoginUserForm, PasswordChangeUserForm, RegisterUserForm, UpdateUserForm
from .models import User


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
        user.hashed_password = services.create_hashed_password(form.data["password1"])
        user.save()

        login(self.request, user, backend='django.contrib.auth.backends.CustomAuthBackend')
        
        tasks.send_registration_message.delay(user.email)
        return redirect('news')


class ProfileUser(DataMixin, DetailView):
    model = User
    template_name = 'users/profile.html'
    pk_url_kwarg = 'user_pk'
    context_object_name = "my_profile"

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        self.object = self.get_object()

        if self.object.id != request.user.id:
            raise PermissionDenied()
                
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["social_prefix"] = settings.SOCIAL_PREFIX
        return context | self.get_context(title='My profile')


def logout_view(request):
    logout(request)
    return redirect('news')


class LoginUser(LoginView):
    template_name = 'users/login.html'
    form_class = LoginUserForm

    def post(self, request: HttpRequest, *args: str, **kwargs) -> HttpResponse:
        form = self.get_form()
        if form.is_valid():
            user = db_queries.get_user_or_none(form.data["username"])
            
            # additional verification 
            services.ValidateCustomPassword().check_custom_password("password", user, form)
            
            if form.errors:
                return self.form_invalid(form)

            return self.form_valid(form)
        return self.form_invalid(form)

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
    
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        self.object = self.get_object()

        if self.object.id != request.user.id or settings.SOCIAL_PREFIX in self.object.slug:
            raise PermissionDenied()
                
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def post(self, request: HttpRequest, *args: str, **kwargs) -> HttpResponse:
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            # additional verification
            error_mes = "Old password is incorrect!"
            services.ValidateCustomPassword(error_mes).check_custom_password("old_password", self.object, form)

            if form.errors:
                return self.form_invalid(form)
            return self.form_valid(form)

        return self.form_invalid(form)
    
    def form_valid(self, form) -> HttpResponse:
        user = form.save()
        user.hashed_password = services.create_hashed_password(form.data["new_password1"])
        user.save()
        return super().form_valid(form)


class UpdateUserView(DataMixin, UpdateView):
    model = User
    form_class = UpdateUserForm
    template_name = 'users/edit_profile.html'
    slug_url_kwarg = 'slug'
    context_object_name = "my_profile"

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        self.object = self.get_object()

        if self.object.id != request.user.id or settings.SOCIAL_PREFIX in self.object.slug:
            raise PermissionDenied()
                
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context | self.get_context(title='Change profile', button='Submit')
