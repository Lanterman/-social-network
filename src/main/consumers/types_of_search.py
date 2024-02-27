from . import db_queries


class SearchForSubscriptions:
    """Search for subscriptions"""

    @staticmethod
    def create_sub_list(subs) -> list:
        """Create sub list"""

        sub_list = []

        for sub in subs:
                sub_list.append({
                    "user_pk": sub.subscription_id.id,
                    "user_url": sub.subscription_id.get_absolute_url(),
                    "user_full_name": sub.subscription_id.get_full_name().title(),
                    "user_photo": sub.subscription_id.photo.url if sub.subscription_id.photo else None,
                })
        
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

        for sub in users:
                user_list.append({
                    "user_pk": sub.id,
                    "user_url": sub.get_absolute_url(),
                    "user_full_name": sub.get_full_name().title(),
                    "user_photo": sub.photo.url if sub.photo else None
                })
        
        return user_list
    
    @staticmethod
    def find_subs_from_global_search(global_users: list, subs: list) -> None:
         """
         Find my subscriptions in global user search.
         If they exist, add the my_subs element to their dictionary.
         """

         for user in global_users:
             if user in subs:
                  user["my_sub"] = True

    async def _global_users_search(self, search_value: str, user_id: int, subs: list) -> list:
        """Searching, processing and returning a list of users"""

        global_users = await db_queries.users_search(search_value, user_id)
        global_user_list = self.create_user_list(global_users)
        
        self.find_subs_from_global_search(global_user_list, subs)

        return global_user_list
