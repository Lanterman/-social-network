import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from main.models import Comments
from users.models import Message, Users


class ChatConsumer(WebsocketConsumer):
    """The consumer of the chat"""

    def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.room_group_name = 'chat_%s' % self.chat_id
        # Join room group
        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        chat_id = text_data_json["chat_id"]
        user_pk = text_data_json["user_pk"]
        self.message_obj = Message.objects.create(message=message, chat_id=chat_id, author_id=user_pk)
        user = Users.objects.get(pk=user_pk)
        full_name = user.get_full_name()
        author_name = full_name if full_name else user.username
        message_info = {
            "message": message,
            "pub_date": "Только что",
            "is_readed": "messages_us" if self.message_obj.is_readed else "unreaded",
            "author_name": author_name if len(author_name) < 50 else author_name[:50] + "...",
            "author_url": user.get_absolute_url(),
            "author_photo": user.photo.url if user.photo else "/media/users/slen/slen.png/"
        }
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {'type': 'chat_message', 'message_info': message_info}
        )

    # Receive message from room group
    def chat_message(self, event):
        message_info = event['message_info']
        # Send message to WebSocket
        self.send(text_data=json.dumps({'message_info': message_info}))


class CommentConsumer(WebsocketConsumer):
    """The consumer of the comment"""

    def connect(self):
        self.publish_slug = self.scope['url_route']['kwargs']['publish_slug']
        self.publication_comments_group = 'publication_comments_%s' % self.publish_slug
        # Join room group
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
            async_to_sync(self.channel_layer.group_send)(
                self.publication_comments_group,
                {'type': 'comment_like', 'likes_info': data, 'action_type': "action_like"}
            )
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

    def comment_like(self, event):
        likes_info = event["likes_info"]
        action_like = event["action_type"]
        self.send(text_data=json.dumps({"likes_info": likes_info, "action_type": action_like}))

    def show_comment(self, event):
        comment_info = event["comment_info"]
        create_comment = event["action_type"]
        self.send(text_data=json.dumps({"comment_info": comment_info, "action_type": create_comment}))
