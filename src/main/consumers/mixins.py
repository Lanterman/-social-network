import logging

from channels.db import database_sync_to_async

from src.users.models import Follower, User


class ConfirmFollower:
    """Confirm follower mixin"""

    @staticmethod
    def get_follower_full_name(follower: User) -> str:
        """Get follower full name"""

        full_name = follower.get_full_name()

        if full_name:
            return f"{full_name[:21].title()}..." if len(full_name) > 20 else full_name.title()
        return "Anonymous"

    @database_sync_to_async
    def conf_follower(self, follower_id: int):
        checked_follower = User.objects.get(id=follower_id)
        
        output_data = {
            "follower_id": follower_id,   
            "follower_photo": None if not checked_follower.photo else checked_follower.photo.url,
            "follower_full_name": self.get_follower_full_name(checked_follower),
            "follower_url": checked_follower.get_absolute_url()
        }
        return output_data