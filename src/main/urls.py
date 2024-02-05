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
    path('groups/<slug:group_slug>/add_published/', AddPublished.as_view(), name='add_published'),
    path('publish/<slug:publish_slug>/', DetailPublication.as_view(), name='detail_publish'),
    path('publish/<slug:publish_slug>/comments/', PublishedCommentsView.as_view(), name='comments'),
    # logic
    path('groups/<slug:group_slug>/del_group/', del_group, name='del_group'),  # del group
    path('groups/<slug:pub_slug>/<slug:group_slug>/del_published/', del_pub_group, name='del_pub_group'),  # del pub_group
    path('groups/<slug:pub_slug>/del_published/', del_published, name='del_published'),  # del published
    path('groups/<slug:group_slug>/update_group/', UpdateGroup.as_view(), name='update_group'),  # update group
    path('groups/<slug:pub_slug>/update_pub/', UpdatePublished.as_view(), name='update_pub'),  # update published

    ### create with js
    path('home/<int:follower_id>/confirm_follower/', conf_follower, name='conf_follower'),  # confirm follower
    path('home/<int:follower_id>/cancel_follower/', cancel_follower, name='conf_follower'),  # cancel follower

    ###
    path('groups/<int:user_pk>/friend_hide/', friend_hide, name='friend_hide'),  # hide friend
    path('groups/<int:user_pk>/friend_del_primary/', friend_del_primary, name='friend_del_primary'),  # del friend primary
    path('groups/<slug:group_slug>/group_activity/', group_activity, name='group_activity'),  # group activity
    path('groups/<slug:group_slug>/quit_primary/', group_quit_primary, name='group_quit_primary'),  # quit_primary
    path("add-rating/", AddStarRating.as_view(), name='add_rating'),  # star_rating

    ### greacte with ws
    path('p/', SearchPublished.as_view(), name='search_published'),  # news_search 
    path('g/', SearchGroups.as_view(), name='search_group'),  # group_search
    path('m/', SearchMessages.as_view(), name='search_messages'),  # search_messages
    path('f-<int:user_pk>/', SearchFollowers.as_view(), name='search_followers'),  # followers_search
    path('s-<int:user_pk>/', SearchSubscriptions.as_view(), name='search_subscriptions'),  # subscriptions_search
]
