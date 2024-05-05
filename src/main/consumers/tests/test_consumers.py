from django.urls import path, re_path
from django.test.testcases import TransactionTestCase
from channels.auth import AuthMiddlewareStack
from channels.routing import URLRouter
from channels.testing import WebsocketCommunicator
from channels.db import database_sync_to_async

from src.main.consumers import consumers
from src.main import models
from src.users import models as user_models
from config.settings import redis_instance


application = AuthMiddlewareStack(
    URLRouter([
        path('ws/news/', consumers.NewsPageConsumer.as_asgi()),
        path('ws/home/', consumers.HomePageConsumer.as_asgi()),
        path('ws/messengers/', consumers.MessengersPageConsumer.as_asgi()),
        re_path(r'ws/messages/chat/(?P<chat_id>\w+)/$', consumers.ChatConsumer.as_asgi()),
        path('ws/followers/', consumers.FollowerConsumer.as_asgi()),
        path('ws/subscriptions/', consumers.SubscriptionConsumer.as_asgi()),
        path('ws/groups/', consumers.GroupsPageConsumer.as_asgi()),
        path('ws/publication/<publication_id>/comments/', consumers.CommentConsumer.as_asgi()),
    ]
))


class Config(TransactionTestCase):

    fixtures = ["./config/tests/test_data.json"]
    
    def setUp(self):
        super().setUp()
        self.user_1 = user_models.User.objects.get(id=1)
        self.user_3 = user_models.User.objects.get(id=3)
        
    def tearDown(self) -> None:
        redis_instance.flushall()
        super().tearDown()

    async def launch_websocket_communicator(self, path: str):
        """Launch websocket communicator"""

        communicator = WebsocketCommunicator(application, path)
        connected, sub_protocol = await communicator.connect()
        assert connected
        assert sub_protocol is None
        return communicator


# class TestMainConsumer(Config):
#     """Testing MainConsumer consumer"""

#     def setUp(self):
#         super().setUp()
#         self.lobby_1 = models.Lobby.objects.get(id=1)
#         self.lobby_2 = models.Lobby.objects.get(id=2)
    
#     async def test_created_game(self):
#         """Testing created_game event"""

#         path_1 = f"ws/main/?token={self.token_1.access_token}"
#         path_2 = f"ws/main/?token={self.token_3.access_token}"
#         communicator_1 = await self.launch_websocket_communicator(path=path_1)
#         communicator_2 = await self.launch_websocket_communicator(path=path_2)
#         assert communicator_1.scope["user"].id == self.user_1.id, communicator_1.scope["user"].id

#         await communicator_1.send_json_to({"type": "created_game", "lobby_slug": str(self.lobby_1.slug)})
#         response_1 = await communicator_1.receive_nothing()
#         response_2 = await communicator_2.receive_json_from()
#         assert response_1 == True, response_1
#         assert response_2 == {"type": "created_game", "lobby": self.ser_lobby_1, "user_id": self.user_1.id}, response_2

#         await communicator_1.disconnect()
#         await communicator_2.disconnect()
        