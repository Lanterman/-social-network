from . import db_queries

from . import serializers


class SearchForPublications:
    """Search for publications"""
    
    async def _search_for_publications(self, search_value: str) -> list:
        """Searching, processing and returning a list of publications"""

        publications = await db_queries.get_publications_by_search(search_value)
        publications_list = serializers.PublicationSerialazer(publications, many=True)
        return publications_list.data


class SearchForFollowers:
    """Search for followers"""

    async def _search_for_followers(self, search_value: str, user_id: int) -> list:
        """Searching, processing and returning a list of followers"""

        followers = await db_queries.get_followers_search(search_value, user_id)
        followers_list = serializers.FollowerSearchSerialazer(followers, many=True)
        return followers_list.data


class SearchForSubscriptions:
    """Search for subscriptions"""

    async def _search_for_subscriptions(self, search_value: str, user_id: int) -> list:
        """Searching, processing and returning a list of subscriptions"""

        subs = await db_queries.get_subs_search(search_value, user_id)
        sub_list = serializers.SubscriptionsSearchSerialazer(subs, many=True)
        return sub_list.data


class GlobalSearch:
    """Global Search"""
    
    @staticmethod
    def find_connections_from_global_search(global_users: list, subs: list, followers: list) -> None:
        """
        Find my followers and my subs in global user search.
        If I is following a user, add the my_sub element to their dictionary.
        If a user is following me, add the my_followers element to their dictionary.
        """

        for user in global_users:
            if user in subs and user in followers:
                user["my_sub"] = True
                user["my_follower"] = True

            elif user in followers:
                user["my_follower"] = True
            
            elif user in subs:
                 user["my_sub"] = True
    
    @staticmethod
    def find_subs_from_global_search(global_users: list, subs: list) -> None:
         """
         Find my subscriptions in global user search.
         If they exist, add the my_subs element to their dictionary.
         """

         for user in global_users:
             if user in subs:
                  user["my_sub"] = True

    async def _search_for_global_users(self, search_value: str, user_id: int, subs: list, followers: list) -> list:
        """Searching, processing and returning a list of users"""

        global_users = await db_queries.get_users_search(search_value, user_id)
        global_user_list = serializers.UserSearchSerialazer(global_users, many=True).data

        if followers:
            self.find_connections_from_global_search(global_user_list, subs, followers)
        else:
            self.find_subs_from_global_search(global_user_list, subs)

        return global_user_list
