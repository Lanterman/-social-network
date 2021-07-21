from django.urls import path

from main.views import *

urlpatterns = [
    path('', news, name='news'),
    path('home/', home, name='home'),
    path('messages/', messages, name='messages'),
    path('friends/', friends, name='friends'),
    path('groups/', groups, name='groups'),
    path('groups/<slug:group_slug>/', DetailGroup.as_view(), name='detail_group'),
    path('publish/<slug:publish_slug>/', DetailPublish.as_view(), name='detail_publish'),
    path('publish/<slug:publish_slug>/comments/', PublishedCommentsView.as_view(), name='comments'),
    path('publish/<slug:publish_slug>/add_comment/', AddCommentView.as_view(), name='add_comment'),
    path('publish/comments/<slug:users_slug>/', AddCommentView.as_view(), name='add_user_comment'),  # Уточнить

]
