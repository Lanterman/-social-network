from django.urls import path, include


urlpatterns = [
    path('', include('src.main.urls')),
    path('users/', include('src.users.urls')),
]