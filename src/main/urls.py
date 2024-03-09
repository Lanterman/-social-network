from django.urls import path, re_path

from src.main.views import *

urlpatterns = [
    path('', NewsView.as_view(), name='news'),
    path('home/<int:user_pk>/', HomeView.as_view(), name='home'),
    path('messages/<int:user_pk>/', MessagesView.as_view(), name='messages'),
    path('chat/<int:chat_id>/', ChatDetailView.as_view(), name='chat'),
    path('messages/check/<int:user_id>/', CreateDialogView.as_view(), name='check'),
    path('followers/<int:user_pk>/', FollowersView.as_view(), name='followers'),
    path('subscriptions/<int:user_pk>/', SubscriptionsView.as_view(), name='subscriptions'),
    path('groups/<int:user_pk>/', GroupsView.as_view(), name='groups'),
    path('groups/add_group/', AddGroup.as_view(), name='add_group'),
    path('groups/<slug:group_slug>/', DetailGroupView.as_view(), name='detail_group'),
    path('groups/<slug:group_slug>/add_publication/', AddPublication.as_view(), name='add_publication'),
    path('publish/<slug:publish_slug>/', DetailPublication.as_view(), name='detail_publish'),
    path('publish/<slug:publish_slug>/comments/', PublicationCommentsView.as_view(), name='comments'),
    
    # logic
    path('groups/<slug:group_slug>/del_group/', del_group, name='del_group'),  # del group
    path('groups/<int:pub_id>/del_publication/', delete_publication, name='delete_publication'),  # delete publication
    path('groups/<slug:group_slug>/update_group/', UpdateGroup.as_view(), name='update_group'),  # update group
    path('groups/<slug:pub_slug>/update_pub/', UpdatePublished.as_view(), name='update_pub'),  # update published
    path('groups/<int:group_id>/group_activity/', group_activity, name='group_activity'),  # group activity
    path("add-rating/", AddStarRating.as_view(), name='add_rating'),  # star_rating

    ### greacte with ws
    path('m/', SearchMessages.as_view(), name='search_messages'),  # search_messages
]
