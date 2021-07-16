from django.urls import path

from main.views import *

urlpatterns = [
    path('', news, name='news'),
    path('home/', home, name='home'),
    path('messages/', messages, name='messages'),
    path('friends/', friends, name='friends'),
    path('groups/', groups, name='groups'),
    path('groups/<slug:group_slug>/', detail_group, name='detail_group'),
    path('publish/<slug:publish_slug>/comments/', CommentsPublished.as_view(), name='comments'),
    path('publish/<slug:publish_slug>/', DetailPublish.as_view(), name='detail_publish'),
]
