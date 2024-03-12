from datetime import datetime

from rest_framework.serializers import ModelSerializer

from src.main.models import Publication, Group
from src.users.models import User, Chat, Message


# base serializers
class FormattingClass:
    """Class that formats field values"""

    @staticmethod
    def get_short_field_value(value: str, counted_elems: int = 10) -> str:
        """If a field value is longer than 'counted_elems', shorten it."""

        return f"{value[:counted_elems]}..." if len(value) > counted_elems else value
    
    @staticmethod
    def get_formatted_date(date: datetime) -> datetime:
        """Get a formatted date"""

        formatted_date = date.strftime("%d.%m.%Y, %H:%M:%S")
        return formatted_date
    
    @staticmethod
    def get_formatted_user_full_name(full_name: User, counted_elems: int = 20) -> str:
        """Get a formatted user full name"""

        if full_name:
            return f"{full_name[:counted_elems].title()}..." if len(full_name) > counted_elems else full_name.title()
        return "Anonymous"


# extra serializers
class UserForPublication(ModelSerializer):
    """The user serializator for a publication (PublicationSerialazer)"""

    class Meta:
        model = User
        fields = ["id", "username"]
    
    def to_representation(self, instance):
        instance.username = FormattingClass.get_short_field_value(instance.username)
        ret = super().to_representation(instance)
        ret["user_url"] = instance.get_absolute_url()
        return ret


class MemberForChatSerialazer(ModelSerializer):
    """The member for chat serializer for chat (ChatSearchSerializer)"""

    class Meta:
        model = User
        fields = ("id", "photo")
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["user_full_name"] = FormattingClass.get_formatted_user_full_name(instance.get_full_name(), 40)
        ret["user_url"] = instance.get_absolute_url()
        return ret


class LastChatMessage(ModelSerializer):
    """The last chat message serializer for chat (ChatSearchSerializer)"""

    class Meta:
        model = Message
        fields = ("id", "author_id", "message", "pub_date", "is_readed")
    
    def to_representation(self, instance):
        instance.pub_date = FormattingClass.get_formatted_date(instance.pub_date)
        return super().to_representation(instance)


# A serializer for a home page 
class ConfirmFollowerSerialazer(ModelSerializer):
    """The serializer is designed to convert the confirmated user"""

    class Meta:
        model = User
        fields = ("id", "photo")
        
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["user_full_name"] = FormattingClass.get_formatted_user_full_name(instance.get_full_name())
        ret["user_url"] = instance.get_absolute_url()
        return ret


# All types of search serializers
class PublicationSearchSerialazer(ModelSerializer):
    """The serializer is designed to convert the publication"""

    owner = UserForPublication()

    class Meta:
        model = Publication
        fields = ("id", "name", "slug", "biography", "date", "owner", "photo")
    
    @staticmethod
    def get_formatted_biography(biography: str, counted_elems: int = 200) -> str:
        """Get a formatted biography"""

        f_biography = biography.replace(r"<", "< ").replace("\n", "</br>")
        counted_output_elems = f_biography[:counted_elems].count("</br>") * 4 + counted_elems
        return FormattingClass.get_short_field_value(f_biography, counted_output_elems)
    
    def to_representation(self, instance):
        instance.name = FormattingClass.get_short_field_value(instance.name, 30).title()
        instance.biography = self.get_formatted_biography(instance.biography)
        instance.date = FormattingClass.get_formatted_date(instance.date)

        ret = super().to_representation(instance)
        ret["rating"] = instance.rat
        ret["publication_url"] = instance.get_absolute_url()
        return ret


class ChatSearchSerialazer(ModelSerializer):
    """
    The chat serializer is designed to convert groups to display in search.
    Last message of chats
    """

    members = MemberForChatSerialazer(many=True)
    message_set = LastChatMessage(many=True)

    class Meta:
        model = Chat
        fields = ("id", "members", "message_set")
    
    @staticmethod
    def get_formatted_last_message(message_dict: dict, counted_elems: int = 80) -> dict:
        """Get a formatted last message of a chat"""

        f_message = message_dict["message"].replace(r"<", "< ")
        message_dict["message"] = FormattingClass.get_short_field_value(f_message, counted_elems)
        return message_dict
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["chat_url"] = instance.get_absolute_url()
        ret["last_message"] = self.get_formatted_last_message(ret["message_set"][0])
        return ret


class UserSearchSerialazer(ModelSerializer):
    """The basic serializer is designed to convert users to display in search"""

    class Meta:
        model = User
        fields = ("id", "photo")
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["user_full_name"] = instance.get_full_name()
        ret["user_url"] = instance.get_absolute_url()
        return ret


class FollowerSearchSerialazer(UserSearchSerialazer):
    """The serializer is designed to convert followers to display in search"""
    
    def to_representation(self, instance):
        return super().to_representation(instance.follower_id)


class SubscriptionsSearchSerialazer(UserSearchSerialazer):
    """The serializer is designed to convert subscriptions to display in search"""
    
    def to_representation(self, instance):
        return super().to_representation(instance.subscription_id)


class GroupsSearchSerialazer(ModelSerializer):
    """The group serializer is designed to convert groups to display in search"""

    class Meta:
        model = Group
        fields = ("id", "name", "photo", "owner", "followers")
    
    def to_representation(self, instance):
        instance.name = instance.name.title()

        ret = super().to_representation(instance)
        ret["group_url"] = instance.get_absolute_url()
        return ret
