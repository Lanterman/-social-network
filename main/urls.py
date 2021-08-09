from django.urls import path

from main.views import *

urlpatterns = [
    path('', NewsView.as_view(), name='news'),
    path('home/<int:user_pk>/', HomeView.as_view(), name='home'),
    path('messages/<int:user_pk>/', messages, name='messages'),
    path('friends/<int:user_pk>/', friends, name='friends'),
    path('groups/<int:user_pk>/', GroupsView.as_view(), name='groups'),
    path('groups/<slug:group_slug>/quit/', group_quit, name='group_quit'),  # quit
    path('groups/<slug:group_slug>/enter/', group_enter, name='group_enter'),  # entry
    path('groups/add_group/', AddGroup.as_view(), name='add_group'),
    path('groups/<slug:group_slug>/', DetailGroupView.as_view(), name='detail_group'),
    path('groups/<slug:group_slug>/add_published/', AddPublished.as_view(), name='add_published'),
    path('publish/<slug:publish_slug>/', DetailPublish.as_view(), name='detail_publish'),
    path('publish/<slug:publish_slug>/comments/', PublishedCommentsView.as_view(), name='comments'),
    path('publish/<slug:publish_slug>/add_comment/', AddCommentView.as_view(), name='add_comment'),
    path("add-rating/", AddStarRating.as_view(), name='add_rating'),
]
