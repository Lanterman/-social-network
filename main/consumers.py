import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from users.models import Message, Chat, Users


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
        # chat = Chat.objects.get(id=chat_id).members.all()
        # if chat[0].pk == user_pk:
        #     user = chat[1]
        # else:
         #     user = chat[0]
        # user_name = user.get_full_name()
        # if not user_name:
        #     user_name = user.username
        # tasks.send_message.delay(user_name, user.email, chat_id)

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
