from datetime import datetime

from rest_framework.serializers import ModelSerializer

from src.main.models import Publication
from src.users.models import User


class UserForPublication(ModelSerializer):
    """The user serializator for a publication (PublicationSerialazer)"""

    class Meta:
        model = User
        fields = ["id", "username"]
    
    def to_representation(self, instance):
        instance.username = f"{instance.username[:11]}..." if len(instance.username) > 10 else instance.username
        ret = super().to_representation(instance)
        ret["user_url"] = instance.get_absolute_url()
        return ret


class PublicationSerialazer(ModelSerializer):
    """The serializer is designed to convert the publication"""

    owner = UserForPublication()

    class Meta:
        model = Publication
        fields = ("id", "name", "slug", "biography", "date", "owner", "photo")
    
    @staticmethod
    def get_formatted_name(name: str) -> str:
        """Get a formatted name"""

        return f"{name[:31].title()}..." if len(name) > 30 else name.title()
    
    @staticmethod
    def get_formatted_biography(biography: str, counted_elems: int = 200) -> str:
        """Get a formatted biography"""

        f_biography = biography.replace(r"<", "< ").replace("\n", "</br>")
        counted_output_elems = f_biography[:201].count("</br>") * 4 + counted_elems
        return f"{f_biography[:counted_output_elems]}..." if len(f_biography) > counted_elems else f_biography
    
    @staticmethod
    def get_formatted_date(date: datetime) -> str:
        """Get a formatted date"""

        formatted_date = date.strftime("%d.%m.%Y, %H:%M:%S")
        return formatted_date
    
    def to_representation(self, instance):
        instance.name = self.get_formatted_name(instance.name)
        instance.biography = self.get_formatted_biography(instance.biography)
        instance.date = self.get_formatted_date(instance.date)

        ret = super().to_representation(instance)
        ret["rating"] = instance.rat
        ret["publication_url"] = instance.get_absolute_url()
        return ret


class ConfirmFollowerSerialazer(ModelSerializer):
    """The serializer is designed to convert the confirmated user"""

    class Meta:
        model = User
        fields = ("id", "photo")
    
    @staticmethod
    def get_follower_full_name(follower: User) -> str:
        """Get follower full name"""

        full_name = follower.get_full_name()

        if full_name:
            return f"{full_name[:21].title()}..." if len(full_name) > 20 else full_name.title()
        return "Anonymous"
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["user_full_name"] = self.get_follower_full_name(instance)
        ret["user_url"] = instance.get_absolute_url()
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
