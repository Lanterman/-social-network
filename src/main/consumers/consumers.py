import json
import logging

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer

from . import db_queries, mixins, serializers
from src.main.models import Comment


class NewsPageConsumer(AsyncWebsocketConsumer, mixins.AllTypesOfSearch):
    """
    The consumer of the news page.
    1. Search publications.
    """

    async def connect(self):
        self.user = self.scope['user']
        self.room_group_name = f'news_{self.user.id}'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
    

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)

        # search for publications --- response exists
        if data["event_type"] == "search":
            publications = await self.search_for_publications(data["search_value"])
            output_data= {'event_type': 'search', 'publications': publications, "user_id": self.user.id}
            await self.send(text_data=json.dumps(output_data))


class HomePageConsumer(AsyncWebsocketConsumer, mixins.ConfirmFollower):
    """
    The consumer of the home page.
    1. Confirm or cancel new subscribers.
    2. Removing subscribers and subscriptions.
    3. Subscribe, unsubscribe and block users.
    """

    async def connect(self):
        self.user = self.scope['user']
        self.room_group_name = f'home_{self.user.id}'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
    

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)

        # confrim follower (follower modal - announcement) --- response exists
        if data["event_type"] == "confirm_follower":
            await db_queries.confirm_follower(data["follower_id"], self.user.id)
            checked_follower = await self.conf_follower(data["follower_id"])
            await self.send(text_data=json.dumps({
                "follower": checked_follower, 
                "event_type": "confirm_follower",
                "user_id": self.user.id
            }))
        
        # cancel follower (follower modal - announcement)
        elif data["event_type"] == "cancel_follower":
            await db_queries.remove_follower_instance_by_follower_id(data["follower_id"], self.user.id)
        
        # remove follower (follower modal - old followers) --- response exists
        elif data["event_type"] == "remove_follower":
            await db_queries.remove_follower_instance_by_follower_id(data["follower_id"], self.user.id)
            await self.send(text_data=json.dumps({"event_type": "remove_follower"}))
        
        # confrim subscription (subscription modal) --- response exists
        elif data["event_type"] == "remove_subscription":
            await db_queries.remove_follower_instance_by_sub_id(data["subscription_id"], self.user.id)
            await self.send(text_data=json.dumps({"event_type": "remove_subscription"}))
        
        # subscribe to another user --- response exists
        elif data["event_type"] == "sub_user":
            await db_queries.create_follower_instance_by_sub_id(data["user_id"], self.user.id)
            await self.send(text_data=json.dumps(data))
        
        # unsubscribe from another user --- response exists
        elif data["event_type"] == "unsub_user":
            await db_queries.remove_follower_instance_by_sub_id(data["user_id"], self.user.id)
            await self.send(text_data=json.dumps(data))

        # block another user
        elif data["event_type"] == "block_user":
            await db_queries.remove_follower_instance_by_follower_id(data["user_id"], self.user.id)


class FollowerConsumer(AsyncWebsocketConsumer, mixins.AllTypesOfSearch):
    """
    The consumer of the follower page.
    1. Block and subscribe user.
    2. Search my followers and global users.
    """

    async def connect(self):
        self.user = self.scope['user']
        self.room_group_name = f'{self.user.id}_follower'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
    

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)

        # unsubscribe --- doesn't send anything
        if data["event_type"] == "block_user":
            await db_queries.remove_follower_instances(data["user_id"], self.user.id)
        
        # unsubscribe --- doesn't send anything
        elif data["event_type"] == "unsubscribe":
            await db_queries.remove_follower_instance_by_sub_id(data["user_id"], self.user.id)

        # subscribe --- doesn't send anything
        elif data["event_type"] == "subscribe":
            await db_queries.create_follower_instance_by_sub_id(data["user_id"], self.user.id)

        # search for subscriptions and global users search --- response exists
        elif data["event_type"] == "search":
            my_subs = await self.search_for_subscriptions(data["search_value"], self.user.id)
            my_followers = await self.search_for_followers(data["search_value"], self.user.id)
            global_users = await self.search_for_global_users(data["search_value"], self.user.id, my_subs, my_followers)
            await self.send(text_data=json.dumps(
                {'event_type': 'search', 'my_followers': my_followers, "global_users": global_users})
            )


class SubscriptionConsumer(AsyncWebsocketConsumer, mixins.AllTypesOfSearch):
    """
    The consumer of the subscriptions page.
    1. Unsubscribe and subscribe user.
    2. Search my subscribers and global users.
    """

    async def connect(self):
        self.user = self.scope['user']
        self.room_group_name = f'{self.user.id}_sub'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
    

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)

        # unsubscribe --- doesn't send anything
        if data["event_type"] == "unsubscribe":
            await db_queries.remove_follower_instance_by_sub_id(data["subscription_id"], self.user.id)

        # subscribe --- doesn't send anything
        elif data["event_type"] == "subscribe":
            await db_queries.create_follower_instance_by_sub_id(data["subscription_id"], self.user.id)
            new_sub = await db_queries.get_user_by_id(data["subscription_id"])
            dict_of_user = serializers.UserSearchSerialazer(new_sub).data
            await self.send(text_data=json.dumps({"event_type": "subscribe", "new_sub": dict_of_user}))

        # search for subscriptions and global users --- response exists
        elif data["event_type"] == "search":
            my_subs = await self.search_for_subscriptions(data["search_value"], self.user.id)
            global_users = await self.search_for_global_users(data["search_value"], self.user.id, my_subs)
            await self.send(text_data=json.dumps({'event_type': 'search', 'my_subs': my_subs, "global_users": global_users}))


class GroupsPageConsumer(AsyncWebsocketConsumer, mixins.AllTypesOfSearch):
    """
    The consumer of the groups page.
    1. Search groups.
    """

    async def connect(self):
        self.user = self.scope['user']
        self.room_group_name = f'groups_{self.user.id}'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
    

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)

        # search for groups and global groups --- response exists
        if data["event_type"] == "search":
            my_groups = await self.search_for_groups(data["search_value"], self.user.id)
            global_groups = await self.search_for_global_groups(data["search_value"])
            output_data = {
                'event_type': 'search', 
                'my_groups': my_groups, 
                "global_groups": global_groups, 
                "user_id": self.user.id
            }
            await self.send(text_data=json.dumps(output_data))


class ChatConsumer(AsyncWebsocketConsumer):
    """
    The consumer of the chat
    Send message and read unread another user messages
    """

    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.user = self.scope['user']
        self.room_group_name = 'chat_%s' % self.chat_id
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.is_read()
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def is_read(self):
        """Read unread messages"""

        await self.channel_layer.group_send(self.room_group_name, {'type': 'message_read', "user_id": self.user.id})

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        full_name = self.user.get_full_name()
        author_name = full_name if full_name else self.user.username
        message_info = {
            "message": message.replace("\n", "<br>"),
            "author_name": author_name if len(author_name) < 50 else author_name[:50] + "...",
            "author_url": self.user.get_absolute_url(),
            "author_photo": self.user.photo.url if self.user.photo else None
        }

        await self.channel_layer.group_send(
            self.room_group_name,
            {'type': 'chat_message', 'message_info': message_info, "user_id": self.user.id}
        )
        await self.is_read()

    async def message_read(self, event):
        user_id = event["user_id"]
        await self.send(text_data=json.dumps({"message_info": "connect", "user_id": user_id}))

    async def chat_message(self, event):
        message_info = event['message_info']
        user_id = event["user_id"]
        await self.send(text_data=json.dumps({'message_info': message_info, "user_id": user_id}))


class CommentConsumer(WebsocketConsumer):
    """The consumer of the comment"""

    def connect(self):
        self.publication_id = self.scope['url_route']['kwargs']['publication_id']
        self.publication_comments_group = 'publication_comments_%s' % self.publication_id
        self.user = self.scope['user']
        async_to_sync(self.channel_layer.group_add)(self.publication_comments_group, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.publication_comments_group, self.channel_name)

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        if text_data_json["type"] == "like":
            comment_id = text_data_json["comment_id"]
            comment = Comment.objects.prefetch_related('like').get(id=comment_id)
            data = {"like_from_me": 1}
            if self.user in comment.like.all():
                comment.like.remove(self.user)
                data["like_from_me"] = 0
            else:
                comment.like.add(self.user)
            data |= {'comment_id': comment.id, 'likes_count': comment.like.count()}
            self.send(text_data=json.dumps(
                {'likes_info': data, 'action_type': "action_like"}
            ))
        else:
            publication_id = int(text_data_json["publication_id"])
            message = text_data_json["message"]
            comment = Comment.objects.create(biography=message, publication_id_id=publication_id, users_id=self.user.id)
            comment_info = {
                "author_username": self.user.username,
                "author_url": self.user.get_absolute_url(),
                "message": message,
                "comment_id": comment.id,
            }
            async_to_sync(self.channel_layer.group_send)(
                self.publication_comments_group,
                {'type': 'show_comment', 'comment_info': comment_info, 'action_type': "create_comment"}
            )

    def show_comment(self, event):
        comment_info = event["comment_info"]
        create_comment = event["action_type"]
        self.send(text_data=json.dumps({"comment_info": comment_info, "action_type": create_comment}))
