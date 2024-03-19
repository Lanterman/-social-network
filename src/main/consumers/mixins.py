import logging

from channels.db import database_sync_to_async

from src.users.models import User
from . import types_of_search, serializers, db_queries


class ConfirmFollowerMixin:
    """Confirm follower mixin"""

    @database_sync_to_async
    def conf_follower(self, follower_id: int):
        user = serializers.ConfirmFollowerSerialazer(User.objects.get(id=follower_id))
        return user.data


class ChatMessageMixin:
    """Chat message mixin"""

    @staticmethod
    def get_sent_message(message: str, author: User) -> dict:
        """Get a sent chat message"""

        return {
            "message": message.replace("\n", "<br>"),
            "author": serializers.AuthorForChatMessageSerialazer(author).data    
        }


class PublicationCommentMixin:
    """
    Comments on a publication implement the next functions: 
      1. Like a comment 
      2. Create and send a comment
    """

    @database_sync_to_async
    def get_comment_likes_dict(self, comment, is_my_like: int) -> dict:
        """Create and pass comment likes dictionary"""

        return is_my_like | {'comment_id': comment.id, 'likes_count': comment.like.count()}

    @database_sync_to_async
    def add_or_remove_like(self, comment, user: User) -> dict:
        """Add or remove my like"""

        if user in comment.like.all():
            comment.like.remove(user)
            return {"like_from_me": 0}
        
        comment.like.add(user)
        return {"like_from_me": 1}
    
    async def comment_likes_activity(self, comment_id: int, user: User) -> dict:
        """Put or remove a like"""

        comment_db = await db_queries.get_pub_comment_with_likes(comment_id)
        is_my_like = await self.add_or_remove_like(comment_db, user)
        return await self.get_comment_likes_dict(comment_db, is_my_like)

    async def get_comment(self, comment_value: str, publication_id: int, user: User) -> dict:
        """Create and return a new comment"""

        comment_db = await db_queries.create_pub_comment(comment_value, publication_id, user)
        return serializers.CommentOfPublicationSerializer(comment_db).data


class AllTypesOfSearchMixin(types_of_search.SearchForPublicationsMixin,
                            types_of_search.SearchForChatsMixin,
                            types_of_search.SearchForFollowersMixin,
                            types_of_search.SearchForSubscriptionsMixin,
                            types_of_search.GlobalSearchForUserMixin,
                            types_of_search.SearchForGroupsMixin,
                            types_of_search.GlobalSearchForGroupsMixin):
    """
    All types of search:
      1. Search publications  +
      2. Search messages      +
      3. Search followers     +
      4. Search subscriptions +
      5. Global search users  +
      5. Search groups        +
      6. Global search groups +
    """

    async def search_for_publications(self, search_value: str) -> list:
        """Search for publications"""

        return await self._search_for_publications(search_value)
    
    async def search_for_messengers(self, search_value: str, user_id: int) -> list:
        """Search for chats with a last message"""

        return await self._search_for_messengers(search_value, user_id)

    async def search_for_followers(self, search_value: str, user_id: int) -> list:
        """Search for followers"""

        return await self._search_for_followers(search_value, user_id)

    async def search_for_subscriptions(self, search_value: str, user_id: int) -> list:
        """Search for subscriptions"""

        return await self._search_for_subscriptions(search_value, user_id)
    
    async def search_for_global_users(self, search_value: str, user_id: int, subs: list, followers=None) -> list:
        """Search for global user"""

        return await self._search_for_global_users(search_value, user_id, subs, followers)
    
    async def search_for_groups(self, search_value: str, user_id: int) -> list:
        """Search for groups"""

        return await self._search_for_groups(search_value, user_id)
    
    async def search_for_global_groups(self, search_value: str) -> list:
        """Search for globalgroups"""

        return await self._search_for_global_groups(search_value)