import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from main.models import Comments
from users.models import Message, Users


class ChatConsumer(WebsocketConsumer):
    """The consumer of the chat"""

    def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.user = self.scope['user']
        self.room_group_name = 'chat_%s' % self.chat_id
        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)

    def is_readed(self, chat_id, user_id):
        messages = Message.objects.filter(chat_id=chat_id).select_related('author')
        messages.filter(is_readed=False).exclude(author_id=user_id).update(is_readed=True)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {'type': 'message_read', 'message_info': "connect", "user_id": user_id}
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        chat_id = text_data_json["chat_id"]
        user_pk = text_data_json["user_pk"]
        action_type = text_data_json['type']
        if action_type == "add_message":
            message = text_data_json['message']
            full_name = self.user.get_full_name()
            author_name = full_name if full_name else self.user.username
            message_info = {
                "message": message.replace("\n", "<br>"),
                "author_name": author_name if len(author_name) < 50 else author_name[:50] + "...",
                "author_url": self.user.get_absolute_url(),
                "author_photo": self.user.photo.url if self.user.photo else "/media/users/slen/slen.png/"
            }

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {'type': 'chat_message', 'message_info': message_info, "user_id": self.user.id}
            )
        self.is_readed(chat_id=chat_id, user_id=user_pk)

    def message_read(self, event):
        message_info = event["message_info"]
        user_id = event["user_id"]
        self.send(text_data=json.dumps({"message_info": message_info, "user_id": user_id}))

    # Receive message from room group
    def chat_message(self, event):
        message_info = event['message_info']
        user_id = event["user_id"]
        # Send message to WebSocket
        self.send(text_data=json.dumps({'message_info': message_info, "user_id": user_id}))


class CommentConsumer(WebsocketConsumer):
    """The consumer of the comment"""

    def connect(self):
        self.publish_slug = self.scope['url_route']['kwargs']['publish_slug']
        self.publication_comments_group = 'publication_comments_%s' % self.publish_slug
        async_to_sync(self.channel_layer.group_add)(self.publication_comments_group, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.publication_comments_group, self.channel_name)

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        user_id = text_data_json["user_id"]
        if text_data_json["type"] == "like":
            comment_id = text_data_json["comment_id"]
            comment = Comments.objects.prefetch_related('like').get(id=comment_id)
            data = {"like_from_me": 1}
            user = Users.objects.get(id=user_id)
            if user in comment.like.all():
                comment.like.remove(user)
                data["like_from_me"] = 0
            else:
                comment.like.add(user)
            data |= {'comment_id': comment.id, 'likes_count': comment.like.count()}
            self.send(text_data=json.dumps(
                {'likes_info': data, 'action_type': "action_like"}
            ))
        else:
            publish_id = text_data_json["publish_id"]
            message = text_data_json["message"]
            comment = Comments.objects.create(biography=message, published_id=publish_id, users_id=user_id)
            user = Users.objects.get(id=user_id)
            comment_info = {
                "author_username": user.username,
                "author_url": user.get_absolute_url(),
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
