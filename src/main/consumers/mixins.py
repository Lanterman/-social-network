import logging

from channels.db import database_sync_to_async

from src.users.models import Follower, User
from . import types_of_search


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


class AllTypesOfSearch(types_of_search.SearchForSubscriptions,
                       types_of_search.GlobalSearch):
    """
    All types of search:
      1. Search publications
      2. Search messages
      3. Search followers
      4. Search subscriptions +
      5. Global search users  +
      5. Search groups
    """

    async def subscriptions_for_search(self, search_value: str, user_id: int) -> list:
        """Search subscriptions"""

        return await self._subscriptions_for_search(search_value, user_id)
    
    async def global_users_search(self, search_value: str, user_id: int, subs: list) -> list:
        """Global user search"""

        return await self._global_users_search(search_value, user_id, subs)