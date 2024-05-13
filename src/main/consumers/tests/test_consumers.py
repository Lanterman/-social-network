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
        self.user = user_models.User.objects.get(id=3)
        
    def tearDown(self) -> None:
        redis_instance.flushall()
        super().tearDown()

    async def launch_websocket_communicator(self, path: str):
        """Launch websocket communicator"""

        communicator = WebsocketCommunicator(application, path)
        communicator.scope["user"] = self.user
        connected, sub_protocol = await communicator.connect()
        assert connected
        assert sub_protocol is None
        return communicator


class TestNewsPageConsumer(Config):
    """Testing NewsPageConsumer consumer"""
    
    async def test_search(self):
        """Testing search event"""

        communicator = await self.launch_websocket_communicator(f"ws/news/")
        assert communicator.scope["user"] == self.user, communicator.scope["user"]

        await communicator.send_json_to({"event_type": "search", "search_value": "publication"})
        response = await communicator.receive_json_from()
        assert response["event_type"] == "search", response["event_type"]
        assert len(response["publications"]) == 2, len(response["publications"])

        await communicator.send_json_to({"event_type": "search", "search_value": "second"})
        response = await communicator.receive_json_from()
        assert response["event_type"] == "search", response["event_type"]
        assert len(response["publications"]) == 1, len(response["publications"])

        await communicator.send_json_to({"event_type": "search", "search_value": "qw"})
        response = await communicator.receive_json_from()
        assert response["event_type"] == "search", response["event_type"]
        assert len(response["publications"]) == 0, len(response["publications"])

        await communicator.disconnect()


class TestHomePageConsumer(Config):
    """Testing HomePageConsumer consumer"""

    @database_sync_to_async
    def check_confirmation(self, follower_id: str, subscription_id: str) -> None:
        query = user_models.Follower.objects.get(follower_id=follower_id, subscription_id=subscription_id)
        return query.is_checked

    @database_sync_to_async
    def count_instances(self) -> None:
        return user_models.Follower.objects.count()
    
    async def test_confirm_follower(self):
        """Testing confirm_follower event"""

        communicator = await self.launch_websocket_communicator(f"ws/home/")
        assert communicator.scope["user"] == self.user, communicator.scope["user"]
        assert await self.check_confirmation(2, 3) == False, await self.check_confirmation(2, 3)

        await communicator.send_json_to({"event_type": "confirm_follower", "follower_id": 2})
        response = await communicator.receive_json_from()
        assert response["user_id"] == 3, response["user_id"]
        assert response["event_type"] == "confirm_follower", response["event_type"]
        assert response["follower"]["id"] == 2, response["follower"]["id"]
        assert await self.check_confirmation(2, 3) == True, await self.check_confirmation(2, 3)

        await communicator.disconnect()

    async def test_cancel_follower(self):
        """Testing cancel_follower event"""

        communicator = await self.launch_websocket_communicator(f"ws/home/")
        assert communicator.scope["user"] == self.user, communicator.scope["user"]
        assert await self.count_instances() == 3, await self.count_instances()

        await communicator.send_json_to({"event_type": "cancel_follower", "follower_id": 1})
        response = await communicator.receive_nothing()
        assert response == True, response
        assert await self.count_instances() == 2, await self.count_instances()

        await communicator.disconnect()
    
    async def test_remove_follower(self):
        """Testing remove_follower event"""

        communicator = await self.launch_websocket_communicator(f"ws/home/")
        assert communicator.scope["user"] == self.user, communicator.scope["user"]
        assert await self.count_instances() == 3, await self.count_instances()

        await communicator.send_json_to({"event_type": "remove_follower", "follower_id": 1})
        response = await communicator.receive_json_from()
        assert response["event_type"] == "remove_follower", response["event_type"]
        assert await self.count_instances() == 2, await self.count_instances()

        await communicator.disconnect()
    
    async def test_remove_subscription(self):
        """Testing remove_subscription event"""

        communicator = await self.launch_websocket_communicator(f"ws/home/")
        assert communicator.scope["user"] == self.user, communicator.scope["user"]
        assert await self.count_instances() == 3, await self.count_instances()

        await communicator.send_json_to({"event_type": "remove_subscription", "subscription_id": 1})
        response = await communicator.receive_json_from()
        assert response["event_type"] == "remove_subscription", response["event_type"]
        assert await self.count_instances() == 2, await self.count_instances()

        await communicator.disconnect()
    
    async def test_sub_user(self):
        """Testing sub_user event"""

        communicator = await self.launch_websocket_communicator(f"ws/home/")
        assert communicator.scope["user"] == self.user, communicator.scope["user"]
        assert await self.count_instances() == 3, await self.count_instances()

        await communicator.send_json_to({"event_type": "sub_user", "user_id": 1})
        response = await communicator.receive_json_from()
        assert response == {"event_type": "sub_user", "user_id": 1}, response
        assert await self.count_instances() == 4, await self.count_instances()

        await communicator.disconnect()
    
    async def test_unsub_user(self):
        """Testing unsub_user event"""

        communicator = await self.launch_websocket_communicator(f"ws/home/")
        assert communicator.scope["user"] == self.user, communicator.scope["user"]
        assert await self.count_instances() == 3, await self.count_instances()

        await communicator.send_json_to({"event_type": "unsub_user", "user_id": 1})
        response = await communicator.receive_json_from()
        assert response == {"event_type": "unsub_user", "user_id": 1}, response
        assert await self.count_instances() == 2, await self.count_instances()

        await communicator.disconnect()
    
    async def test_block_user(self):
        """Testing block_user event"""

        communicator = await self.launch_websocket_communicator(f"ws/home/")
        assert communicator.scope["user"] == self.user, communicator.scope["user"]
        assert await self.count_instances() == 3, await self.count_instances()

        await communicator.send_json_to({"event_type": "block_user", "user_id": 1})
        response = await communicator.receive_nothing()
        assert response == True, response
        assert await self.count_instances() == 2, await self.count_instances()


class TestMessengersPageConsumer(Config):
    """Testing MessengersPageConsumer consumer"""
    
    async def test_search(self):
        """Testing search event"""

        communicator = await self.launch_websocket_communicator(f"ws/messengers/")
        assert communicator.scope["user"] == self.user, communicator.scope["user"]

        await communicator.send_json_to({"event_type": "search", "search_value": ""})
        response = await communicator.receive_json_from()
        assert response["event_type"] == "search", response["event_type"]
        assert len(response["chats"]) == 1, len(response["chats"])

        await communicator.send_json_to({"event_type": "search", "search_value": "qwe"})
        response = await communicator.receive_json_from()
        assert response["event_type"] == "search", response["event_type"]
        assert len(response["chats"]) == 1, len(response["chats"])

        await communicator.send_json_to({"event_type": "search", "search_value": "q12w"})
        response = await communicator.receive_json_from()
        assert response["event_type"] == "search", response["event_type"]
        assert len(response["chats"]) == 0, len(response["chats"])

        await communicator.disconnect()


class TestFollowerConsumer(Config):
    """Testing FollowerConsumer consumer"""

    @database_sync_to_async
    def count_instances(self) -> None:
        return user_models.Follower.objects.count()
    
    async def test_block_user(self):
        """Testing block_user event"""

        communicator = await self.launch_websocket_communicator(f"ws/followers/")
        assert communicator.scope["user"] == self.user, communicator.scope["user"]
        assert await self.count_instances() == 3, await self.count_instances()

        await communicator.send_json_to({"event_type": "block_user", "user_id": 1})
        response = await communicator.receive_nothing()
        assert response == True, response
        assert await self.count_instances() == 1, await self.count_instances()
    
    async def test_unsubscribe(self):
        """Testing unsubscribe event"""

        communicator = await self.launch_websocket_communicator(f"ws/followers/")
        assert communicator.scope["user"] == self.user, communicator.scope["user"]
        assert await self.count_instances() == 3, await self.count_instances()

        await communicator.send_json_to({"event_type": "unsubscribe", "user_id": 1})
        response = await communicator.receive_nothing()
        assert response == True, response
        assert await self.count_instances() == 2, await self.count_instances()

        await communicator.disconnect()
    
    async def test_subscribe(self):
        """Testing subscribe event"""

        communicator = await self.launch_websocket_communicator(f"ws/followers/")
        assert communicator.scope["user"] == self.user, communicator.scope["user"]
        assert await self.count_instances() == 3, await self.count_instances()

        await communicator.send_json_to({"event_type": "subscribe", "user_id": 1})
        response = await communicator.receive_nothing()
        assert response == True, response
        assert await self.count_instances() == 4, await self.count_instances()

        await communicator.disconnect()
    
    async def test_search(self):
        """Testing search event"""

        communicator = await self.launch_websocket_communicator(f"ws/followers/")
        assert communicator.scope["user"] == self.user, communicator.scope["user"]

        await communicator.send_json_to({"event_type": "search", "search_value": ""})
        response = await communicator.receive_json_from()
        assert response["event_type"] == "search", response["event_type"]
        assert len(response["my_followers"]) == 2, len(response["my_followers"])
        assert len(response["global_users"]) == 2, len(response["global_users"])
        assert response["global_users"][0]["my_sub"] == True, response["global_users"][0]["my_sub"]
        assert response["global_users"][0]["my_follower"] == True, response["global_users"][0]["my_follower"]

        await communicator.send_json_to({"event_type": "search", "search_value": "qw"})
        response = await communicator.receive_json_from()
        assert response["event_type"] == "search", response["event_type"]
        assert len(response["my_followers"]) == 1, len(response["my_followers"])
        assert len(response["global_users"]) == 1, len(response["global_users"])
        assert response["global_users"][0]["my_follower"] == True, response["global_users"][0]["my_follower"]

        await communicator.send_json_to({"event_type": "search", "search_value": "qw1"})
        response = await communicator.receive_json_from()
        assert response["event_type"] == "search", response["event_type"]
        assert len(response["my_followers"]) == 0, len(response["my_followers"])
        assert len(response["global_users"]) == 0, len(response["global_users"])

        await communicator.disconnect()


class TestSubscriptionConsumer(Config):
    """Testing SubscriptionConsumer consumer"""

    @database_sync_to_async
    def count_instances(self) -> None:
        return user_models.Follower.objects.count()
    
    async def test_unsubscribe(self):
        """Testing unsubscribe event"""

        communicator = await self.launch_websocket_communicator(f"ws/subscriptions/")
        assert communicator.scope["user"] == self.user, communicator.scope["user"]
        assert await self.count_instances() == 3, await self.count_instances()

        await communicator.send_json_to({"event_type": "unsubscribe", "subscription_id": 1})
        response = await communicator.receive_nothing()
        assert response == True, response
        assert await self.count_instances() == 2, await self.count_instances()

        await communicator.disconnect()
    
    async def test_subscribe(self):
        """Testing subscribe event"""

        communicator = await self.launch_websocket_communicator(f"ws/subscriptions/")
        assert communicator.scope["user"] == self.user, communicator.scope["user"]
        assert await self.count_instances() == 3, await self.count_instances()

        await communicator.send_json_to({"event_type": "subscribe", "subscription_id": 1})
        response = await communicator.receive_json_from()
        assert response["event_type"] == "subscribe", response["event_type"]
        assert response["new_sub"]["user_url"] == "/home/1/", response["new_sub"]["user_url"]
        assert await self.count_instances() == 4, await self.count_instances()

        await communicator.disconnect()
    
    async def test_search(self):
        """Testing search event"""

        communicator = await self.launch_websocket_communicator(f"ws/subscriptions/")
        assert communicator.scope["user"] == self.user, communicator.scope["user"]

        await communicator.send_json_to({"event_type": "search", "search_value": ""})
        response = await communicator.receive_json_from()
        assert response["event_type"] == "search", response["event_type"]
        assert len(response["my_subs"]) == 1, len(response["my_subs"])
        assert len(response["global_users"]) == 2, len(response["global_users"])
        assert response["global_users"][0]["my_sub"] == True, response["global_users"][0]["my_sub"]

        await communicator.send_json_to({"event_type": "search", "search_value": "qw"})
        response = await communicator.receive_json_from()
        assert response["event_type"] == "search", response["event_type"]
        assert len(response["my_subs"]) == 0, len(response["my_subs"])
        assert len(response["global_users"]) == 1, len(response["global_users"])

        await communicator.disconnect()


class TestGroupsPageConsumer(Config):
    """Testing GroupsPageConsumer consumer"""
    
    async def test_search(self):
        """Testing search event"""

        communicator = await self.launch_websocket_communicator(f"ws/groups/")
        assert communicator.scope["user"] == self.user, communicator.scope["user"]

        await communicator.send_json_to({"event_type": "search", "search_value": "group"})
        response = await communicator.receive_json_from()
        assert response["event_type"] == "search", response["event_type"]
        assert len(response["my_groups"]) == 1, len(response["my_groups"])
        assert len(response["global_groups"]) == 2, len(response["global_groups"])

        await communicator.send_json_to({"event_type": "search", "search_value": "second"})
        response = await communicator.receive_json_from()
        assert response["event_type"] == "search", response["event_type"]
        assert len(response["my_groups"]) == 1, len(response["my_groups"])
        assert len(response["global_groups"]) == 1, len(response["global_groups"])

        await communicator.send_json_to({"event_type": "search", "search_value": "qw"})
        response = await communicator.receive_json_from()
        assert response["event_type"] == "search", response["event_type"]
        assert len(response["my_groups"]) == 0, len(response["my_groups"])
        assert len(response["global_groups"]) == 0, len(response["global_groups"])

        await communicator.disconnect()


class TestChatConsumer(Config):
    """Testing ChatConsumer consumer"""
    
    async def test_send_message(self):
        """Testing send_message event"""

        communicator = await self.launch_websocket_communicator(f"ws/messages/chat/2/")
        assert communicator.scope["user"] == self.user, communicator.scope["user"]

        await communicator.send_json_to({"event_type": "send_message", "message": "group"})
        response = await communicator.receive_json_from()
        assert response["type"] == "send_message", response["type"]
        assert response["message"]["message"] == "group", response["message"]["message"]
        assert response["message"]["author"]["id"] == 3, response["message"]["author"]["id"]

        await communicator.send_json_to({"event_type": "send_message", "message": "message\nIt's good!"})
        response = await communicator.receive_json_from()
        assert response["type"] == "send_message", response["type"]
        assert response["message"]["message"] == "message</br>It's good!", response["message"]["message"]
        assert response["message"]["author"]["id"] == 3, response["message"]["author"]["id"]

        await communicator.disconnect()


class TestCommentConsumer(Config):
    """Testing CommentConsumer consumer"""

    @database_sync_to_async
    def count_instances(self) -> None:
        return models.Comment.objects.count()
    
    @database_sync_to_async
    def count_comment_likes(self, comment_id: int) -> int:
        comment =  models.Comment.objects.get(id=comment_id)
        return comment.like.count()
    
    @database_sync_to_async
    def add_comment_like(self, comment_id: int) -> None:
        comment =  models.Comment.objects.get(id=comment_id)
        comment.like.add(user_models.User.objects.get(id=1))
    
    async def test_send_comment(self):
        """Testing send_comment event"""

        communicator = await self.launch_websocket_communicator(f"ws/publication/1/comments/")
        assert communicator.scope["user"] == self.user, communicator.scope["user"]
        assert await self.count_instances() == 2, await self.count_instances()

        await communicator.send_json_to({"event_type": "send_comment", "comment_value": "group", "publication_id": 1})
        response = await communicator.receive_json_from()
        assert response["type"] == "send_comment", response["type"]
        assert response["comment"]["id"] == 3, response["comment"]["id"]
        assert response["comment"]["biography"] == "group", response["comment"]["biography"]
        assert await self.count_instances() == 3, await self.count_instances()

        await communicator.send_json_to({"event_type": "send_comment", "comment_value": "message\nIt's good!", 
                                         "publication_id": 2})
        response = await communicator.receive_json_from()
        assert response["type"] == "send_comment", response["type"]
        assert response["comment"]["id"] == 4, response["comment"]["id"]
        assert response["comment"]["biography"] == "message\nIt's good!", response["comment"]["biography"]
        assert await self.count_instances() == 4, await self.count_instances()

        await communicator.disconnect()
    
    async def test_like_comment(self):
        """Testing like_comment event"""

        communicator = await self.launch_websocket_communicator(f"ws/publication/1/comments/")
        assert communicator.scope["user"] == self.user, communicator.scope["user"]
        assert await self.count_comment_likes(1) == 0, await self.count_comment_likes(1)

        await communicator.send_json_to({"event_type": "like_comment", "comment_id": 1})
        response = await communicator.receive_json_from()
        assert response["type"] == "like_activity", response["type"]
        assert response["data"]["like_from_me"] == 1, response["data"]["like_from_me"]
        assert response["data"]["likes_count"] == 1, response["data"]["likes_count"]
        assert await self.count_comment_likes(1) == 1, await self.count_comment_likes(1)

        await communicator.send_json_to({"event_type": "like_comment", "comment_id": 1})
        response = await communicator.receive_json_from()
        assert response["type"] == "like_activity", response["type"]
        assert response["data"]["like_from_me"] == 0, response["data"]["like_from_me"]
        assert response["data"]["likes_count"] == 0, response["data"]["likes_count"]
        assert await self.count_comment_likes(1) == 0, await self.count_comment_likes(1)

        await self.add_comment_like(1)
        assert await self.count_comment_likes(1) == 1, await self.count_comment_likes(1)
        await communicator.send_json_to({"event_type": "like_comment", "comment_id": 1})
        response = await communicator.receive_json_from()
        assert response["type"] == "like_activity", response["type"]
        assert response["data"]["like_from_me"] == 1, response["data"]["like_from_me"]
        assert response["data"]["likes_count"] == 2, response["data"]["likes_count"]
        assert await self.count_comment_likes(1) == 2, await self.count_comment_likes(1)

        await communicator.disconnect()
