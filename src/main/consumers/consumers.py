import json
import logging

from channels.generic.websocket import AsyncWebsocketConsumer

from . import db_queries, mixins, serializers


class NewsPageConsumer(AsyncWebsocketConsumer, mixins.AllTypesOfSearchMixin):
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


class HomePageConsumer(AsyncWebsocketConsumer, mixins.ConfirmFollowerMixin):
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


class MessengersPageConsumer(AsyncWebsocketConsumer, mixins.AllTypesOfSearchMixin):
    """
    The consumer of the messengers page.
    1. Search chats.
    """

    async def connect(self):
        self.user = self.scope['user']
        self.room_group_name = f'messengers_{self.user.id}'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
    

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)

        # search for publications --- response exists
        if data["event_type"] == "search":
            chats = await self.search_for_messengers(data["search_value"], self.user.id)
            output_data= {'event_type': 'search', 'chats': chats, "user_id": self.user.id}
            await self.send(text_data=json.dumps(output_data))


class FollowerConsumer(AsyncWebsocketConsumer, mixins.AllTypesOfSearchMixin):
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


class SubscriptionConsumer(AsyncWebsocketConsumer, mixins.AllTypesOfSearchMixin):
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


class GroupsPageConsumer(AsyncWebsocketConsumer, mixins.AllTypesOfSearchMixin):
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


class ChatConsumer(AsyncWebsocketConsumer, mixins.ChatMessageMixin):
    """
    The consumer of the chat
    Send message and read unread another user messages
    """

    async def connect(self):
        self.user = self.scope['user']
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.room_group_name = 'chat_%s' % self.chat_id
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)

        # send new message --- response exists
        if data["event_type"] == "send_message":
            message = self.get_sent_message(data['message'], self.user)
            await self.channel_layer.group_send(self.room_group_name, {'type': 'send_message', "message": message})

    async def send_message(self, data):
        """Send a chat message and read another user(-s) message(-s)"""

        await self.send(text_data=json.dumps(data))


class CommentConsumer(AsyncWebsocketConsumer, mixins.PublicationCommentMixin):
    """The consumer of the comment"""

    async def connect(self):
        self.user = self.scope['user']
        self.publication_id = self.scope['url_route']['kwargs']['publication_id']
        self.pub_comments_group = 'publication_comments_%s' % self.publication_id
        await self.channel_layer.group_add(self.pub_comments_group, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.pub_comments_group, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)

        # send new comment -- response exists
        if data["event_type"] == "send_comment":
            comment = await self.get_comment(data["comment_value"], data["publication_id"], self.user)
            await self.channel_layer.group_send(self.pub_comments_group, {'type': 'send_comment', 'comment': comment})

        # like activity --- response exists
        elif data["event_type"] == "like_comment":
            data = await self.comment_likes_activity(data["comment_id"], self.user)
            await self.send(text_data=json.dumps({'type': "like_activity", "data": data}))

    async def send_comment(self, data):
        """Send a new comment"""

        await self.send(text_data=json.dumps(data))
    
    async def like_activity(self, data):
        """Put on or remove a like"""

        await self.send(text_data=json.dumps(data))
