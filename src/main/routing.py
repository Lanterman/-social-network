from django.urls import re_path

from src.main import consumers

websocket_urlpatterns = [
    re_path(r'ws/messages/chat/(?P<chat_id>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/publish/(?P<publish_slug>\w+)/comments/$', consumers.CommentConsumer.as_asgi()),
]
