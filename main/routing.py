from django.urls import re_path

from main import consumers

websocket_urlpatterns = [
    re_path(r'ws/messages/chat/(?P<chat_id>\w+)/$', consumers.ChatConsumer.as_asgi()),
]
