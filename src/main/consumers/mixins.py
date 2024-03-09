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


class AllTypesOfSearch(types_of_search.SearchForPublications,
                       types_of_search.SearchForFollowers,
                       types_of_search.SearchForSubscriptions,
                       types_of_search.GlobalSearch):
    """
    All types of search:
      1. Search publications  +
      2. Search messages
      3. Search followers     +
      4. Search subscriptions +
      5. Global search users  +
      5. Search groups
    """

    async def search_for_publications(self, search_value: str) -> list:
        """Authorized search for publications and unauthorized search for publications"""

        return await self._search_for_publications(search_value)

    async def search_for_followers(self, search_value: str, user_id: int) -> list:
        """Search for followers"""

        return await self._search_for_followers(search_value, user_id)

    async def search_for_subscriptions(self, search_value: str, user_id: int) -> list:
        """Search for subscriptions"""

        return await self._search_for_subscriptions(search_value, user_id)
    
    async def search_for_global_users(self, search_value: str, user_id: int, subs: list, followers=None) -> list:
        """Search for global user"""

        return await self._search_for_global_users(search_value, user_id, subs, followers)