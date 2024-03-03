from . import db_queries, services


class SearchForFollowers:
    """Search for followers"""

    @staticmethod
    def create_followers_list(followers) -> list:
        """Create followers list"""

        followers_list = []

        for follower in followers:
                followers_list.append(services.create_dict_of_user(follower.follower_id))
        
        return followers_list

    async def _followers_for_search(self, search_value: str, user_id: int) -> list:
        """Searching, processing and returning a list of followers"""

        subs = await db_queries.followers_search(search_value, user_id)
        sub_list = self.create_followers_list(subs)
        return sub_list


class SearchForSubscriptions:
    """Search for subscriptions"""

    @staticmethod
    def create_sub_list(subs) -> list:
        """Create sub list"""

        sub_list = []

        for sub in subs:
                sub_list.append(services.create_dict_of_user(sub.subscription_id))
        
        return sub_list

    async def _subscriptions_for_search(self, search_value: str, user_id: int) -> list:
        """Searching, processing and returning a list of subscriptions"""

        subs = await db_queries.subs_search(search_value, user_id)
        sub_list = self.create_sub_list(subs)
        return sub_list


class GlobalSearch:
    """Global Search"""

    @staticmethod
    def create_user_list(users) -> list:
        """Create user list"""

        user_list = []

        for user in users:
                user_list.append(services.create_dict_of_user(user))
        
        return user_list
    
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

    async def _global_users_search(self, search_value: str, user_id: int, subs: list, followers: list) -> list:
        """Searching, processing and returning a list of users"""

        global_users = await db_queries.users_search(search_value, user_id)
        global_user_list = self.create_user_list(global_users)

        if followers:
            self.find_connections_from_global_search(global_user_list, subs, followers)
        else:
            self.find_subs_from_global_search(global_user_list, subs)

        return global_user_list
