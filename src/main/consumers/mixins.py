import logging

from channels.db import database_sync_to_async

from src.users.models import Follower, User
from . import types_of_search, serializers


class ConfirmFollower:
    """Confirm follower mixin"""

    @database_sync_to_async
    def conf_follower(self, follower_id: int):
        user = serializers.ConfirmFollowerSerialazer(User.objects.get(id=follower_id))
        return user.data


class AllTypesOfSearch(types_of_search.SearchForFollowers,
                       types_of_search.SearchForSubscriptions,
                       types_of_search.GlobalSearch):
    """
    All types of search:
      1. Search publications
      2. Search messages
      3. Search followers     +
      4. Search subscriptions +
      5. Global search users  +
      5. Search groups
    """

    async def followers_for_search(self, search_value: str, user_id: int) -> list:
        """Search followers"""

        return await self._followers_for_search(search_value, user_id)

    async def subscriptions_for_search(self, search_value: str, user_id: int) -> list:
        """Search subscriptions"""

        return await self._subscriptions_for_search(search_value, user_id)
    
    async def global_users_search(self, search_value: str, user_id: int, subs: list, followers=None) -> list:
        """Global user search"""

        return await self._global_users_search(search_value, user_id, subs, followers)