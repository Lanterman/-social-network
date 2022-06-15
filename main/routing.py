from django.urls import re_path

from main import consumers

websocket_urlpatterns = [
    re_path(r'ws/messages/chat/(?P<chat_id>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/publish/(?P<publish_slug1>\w+)/comments/$', consumers.CommentConsumer.as_asgi()),
]
