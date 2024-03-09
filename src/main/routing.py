from django.urls import re_path, path

from src.main.consumers import consumers

websocket_urlpatterns = [
    path('ws/news/', consumers.NewsPageConsumer.as_asgi()),
    path('ws/home/', consumers.HomePageConsumer.as_asgi()),
    re_path(r'ws/messages/chat/(?P<chat_id>\w+)/$', consumers.ChatConsumer.as_asgi()),
    path('ws/followers/', consumers.FollowerConsumer.as_asgi()),
    path('ws/subscriptions/', consumers.SubscriptionConsumer.as_asgi()),
    path('ws/groups/', consumers.GroupsPageConsumer.as_asgi()),
    path('ws/publish/<publication_id>/comments/', consumers.CommentConsumer.as_asgi()),
]
