from django.urls import re_path, path

from src.main import consumers

websocket_urlpatterns = [
    path('ws/home/', consumers.HomeConsumer.as_asgi()),
    re_path(r'ws/messages/chat/(?P<chat_id>\w+)/$', consumers.ChatConsumer.as_asgi()),
    path('ws/publish/<publication_id>/comments/', consumers.CommentConsumer.as_asgi()),
]
