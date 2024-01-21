from django.urls import re_path, path

from src.main import consumers

websocket_urlpatterns = [
    re_path(r'ws/messages/chat/(?P<chat_id>\w+)/$', consumers.ChatConsumer.as_asgi()),
    path('ws/publish/<publication_id>/comments/', consumers.CommentConsumer.as_asgi()),
]
