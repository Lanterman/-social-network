from django.urls import path

from users.views import *

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('profile/<int:user_pk>/', ProfileUser.as_view(), name='profile'),
    path('logout/', logout_view, name='logout'),
    path('login/', LoginUser.as_view(), name='login'),
    path('profile/<slug:slug>/password_change/', PasswordChangeUser.as_view(), name='password_change'),
    path('profile/<slug:slug>/edit_profile/', UpdateUserView.as_view(), name='edit_profile'),
]