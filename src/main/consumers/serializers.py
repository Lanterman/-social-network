from rest_framework.serializers import ModelSerializer

from src.users.models import User


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
