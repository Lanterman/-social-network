from django.urls import path

from main.views import *

urlpatterns = [
    path('', news, name='news'),
    path('home/', home, name='home'),
    path('messages/', messages, name='messages'),
    path('friends/', friends, name='friends'),
    path('groups/', groups, name='groups'),
    path('groups/<slug:group_slug>/quit/', group_quit, name='group_quit'),
    path('groups/<slug:group_slug>/enter/', group_enter, name='group_enter'),
    path('groups/add_group/', AddGroup.as_view(), name='add_group'),
    path('groups/<slug:group_slug>/', detail_group, name='detail_group'),
    path('publish/<slug:publish_slug>/', DetailPublish.as_view(), name='detail_publish'),
    path('publish/<slug:publish_slug>/comments/', PublishedCommentsView.as_view(), name='comments'),
    path('publish/<slug:publish_slug>/add_comment/', add_comment_view, name='add_comment'),
]
