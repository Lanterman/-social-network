from django.urls import path

from main.views import *

urlpatterns = [
    path('', news, name='news'),
    path('home/<int:user_pk>/', HomeView.as_view(), name='home'),
    path('messages/<int:user_pk>/', messages, name='messages'),
    path('friends/<int:user_pk>/', friends, name='friends'),
    path('groups/<int:user_pk>/', groups, name='groups'),
    path('groups/<slug:group_slug>/quit/', group_quit, name='group_quit'),
    path('groups/<slug:group_slug>/enter/', group_enter, name='group_enter'),
    path('groups/add_group/', AddGroup.as_view(), name='add_group'),
    path('groups/<slug:group_slug>/', detail_group, name='detail_group'),
    path('groups/<slug:group_slug>/add_published/', add_published, name='add_published'),
    path('publish/<slug:publish_slug>/', DetailPublish.as_view(), name='detail_publish'),
    path('publish/<slug:publish_slug>/comments/', PublishedCommentsView.as_view(), name='comments'),
    path('publish/<slug:publish_slug>/add_comment/', add_comment_view, name='add_comment'),
]
