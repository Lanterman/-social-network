from django.urls import path

from main.views import *
from users.views import *

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('profile/<slug:username>', profile, name='profile'),
    path('logout/', logout_view, name='logout'),
    path('login/', LoginUser.as_view(), name='login'),
    path('profile/<slug:username>/password_change/', PasswordChangeUser.as_view(), name='password_change'),
    path('profile/<slug:username>/edit_profile/', update, name='edit_profile'),

]