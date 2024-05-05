from django.test import TransactionTestCase

from src.main.consumers import types_of_search, serializers
from src.users import models as user_models


class TestSearchForPublicationsMixin(TransactionTestCase):
    """Testing the SearchForPublicationsMixin class methods"""

    fixtures = ["./config/tests/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.instance = types_of_search.SearchForPublicationsMixin()
    
    async def test__search_for_publications(self):
        ### searching for by the name field the owner field
        response = await self.instance._search_for_publications("admin")
        assert len(response) == 1, len(response)
        assert response[0]["name"] == "Publication", response[0]["name"]
        assert response[0]["owner"]["username"] == "admin", response[0]["owner"]["username"]

        ### searching for by the name field
        response = await self.instance._search_for_publications("second")
        assert len(response) == 1, len(response)
        assert response[0]["name"] == "Second Publication", response[0]["name"]
        assert response[0]["owner"]["username"] == "user", response[0]["owner"]["username"]

        response = await self.instance._search_for_publications("secodn")
        assert len(response) == 0, len(response)


class TestSearchForChatsMixin(TransactionTestCase):
    """Testing the SearchForChatsMixin class methods"""

    fixtures = ["./config/tests/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.instance = types_of_search.SearchForChatsMixin()
    
    async def test__search_for_messengers(self):
        ### searching for by the first_name field
        response = await self.instance._search_for_messengers("qwe", 1)
        assert len(response) == 2, len(response)
        assert response[0]["id"] == 1, response[0]["id"]
        assert len(response[0]["message_set"]) == 1, len(response[0]["message_set"])
        assert response[0]["members"][0]["user_url"] == "/home/2/", response[0]["members"][0]["user_url"]

        ### searching for by the last_name field
        response = await self.instance._search_for_messengers("qwe", 3)
        assert len(response) == 1, len(response)
        assert response[0]["id"] == 2, response[0]["id"]
        assert len(response[0]["message_set"]) == 1, len(response[0]["message_set"])
        assert response[0]["members"][0]["user_url"] == "/home/1/", response[0]["members"][0]["user_url"]

        response = await self.instance._search_for_messengers("qqwe", 3)
        assert len(response) == 0, response


class TestSearchForFollowersMixin(TransactionTestCase):
    """Testing the SearchForFollowersMixin class methods"""

    fixtures = ["./config/tests/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.instance = types_of_search.SearchForFollowersMixin()
    
    async def test__search_for_followers(self):
        response = await self.instance._search_for_followers("lanterm", 1)
        assert len(response) == 1, len(response)
        assert response[0]["id"] == 3, response[0]["id"]
        assert response[0]["user_url"] == "/home/3/", response[0]["user_url"]

        response = await self.instance._search_for_followers("r", 1)
        assert len(response) == 1, len(response)
        assert response[0]["id"] == 3, response[0]["id"]
        assert response[0]["user_url"] == "/home/3/", response[0]["user_url"]

        response = await self.instance._search_for_followers("lanterman", 2)
        assert len(response) == 0, len(response)

        response = await self.instance._search_for_followers("user", 1)
        assert len(response) == 0, len(response)


class TestSearchForSubscriptionsMixin(TransactionTestCase):
    """Testing the SearchForSubscriptionsMixin class methods"""

    fixtures = ["./config/tests/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.instance = types_of_search.SearchForSubscriptionsMixin()
    
    async def test__search_for_subscriptions(self):
        response = await self.instance._search_for_subscriptions("admin", 3)
        assert len(response) == 1, len(response)
        assert response[0]["id"] == 1, response[0]["id"]
        assert response[0]["user_url"] == "/home/1/", response[0]["user_url"]

        response = await self.instance._search_for_subscriptions("r", 1)
        assert len(response) == 1, len(response)
        assert response[0]["id"] == 3, response[0]["id"]
        assert response[0]["user_url"] == "/home/3/", response[0]["user_url"]

        response = await self.instance._search_for_subscriptions("user", 3)
        assert len(response) == 0, len(response)

        response = await self.instance._search_for_subscriptions("admin", 2)
        assert len(response) == 0, len(response)


class TestGlobalSearchForUserMixin(TransactionTestCase):
    """Testing the GlobalSearchForUserMixin class methods"""

    fixtures = ["./config/tests/test_data.json"]

    def setUp(cls) -> None:
        super().setUp()
        cls.user_1 = user_models.User.objects.get(id=1)
        cls.user_2 = user_models.User.objects.get(id=2)
        cls.user_3 = user_models.User.objects.get(id=3)

        cls.user_ser_1 = serializers.UserSearchSerialazer(cls.user_1).data
        cls.user_ser_2 = serializers.UserSearchSerialazer(cls.user_2).data
        cls.user_ser_3 = serializers.UserSearchSerialazer(cls.user_3).data

        cls.instance = types_of_search.GlobalSearchForUserMixin()
    
    def test_find_connections_from_global_search(self):
        self.instance.find_connections_from_global_search(
            [self.user_ser_1, self.user_ser_2], [self.user_ser_1, self.user_ser_2], [self.user_ser_1]
        )
        assert self.user_ser_1["my_sub"] == True, self.user_ser_1
        assert self.user_ser_2["my_sub"] == True, self.user_ser_2
        assert self.user_ser_1["my_follower"] == True, self.user_ser_1

        self.instance.find_connections_from_global_search([self.user_ser_1], [self.user_ser_1], [self.user_ser_2])
        assert self.user_ser_1["my_sub"] == True, self.user_ser_1

        self.instance.find_connections_from_global_search([self.user_ser_1], [self.user_ser_2], [self.user_ser_1])
        assert self.user_ser_1["my_follower"] == True, self.user_ser_1

    def test_find_subs_from_global_search(self):
        self.instance.find_subs_from_global_search(
            [self.user_ser_1, self.user_ser_2], [self.user_ser_1, self.user_ser_2]
        )
        assert self.user_ser_1["my_sub"] == True, self.user_ser_1
        assert self.user_ser_2["my_sub"] == True, self.user_ser_2

    async def test__search_for_global_users(self):
        response = await self.instance._search_for_global_users(
            "r", self.user_1.id, [self.user_ser_2], [self.user_ser_3, self.user_ser_2]
        )

        assert len(response) == 2, len(response)
        assert response[0]["id"] == 3, response[0]["id"]
        assert response[1]["id"] == 2, response[1]["id"]
        assert response[1]["user_url"] == "/home/2/", response[1]["user_url"]
        assert response[0]["my_follower"] == True, response[0]["my_follower"]
        assert response[1]["my_follower"] == True, response[1]["my_follower"]
        assert response[1]["my_sub"] == True, response[1]["my_sub"]

        response = await self.instance._search_for_global_users("r", self.user_1.id, [self.user_ser_3, self.user_ser_2], [])

        assert len(response) == 2, len(response)
        assert response[0]["id"] == 3, response[0]["id"]
        assert response[1]["id"] == 2, response[1]["id"]
        assert response[1]["user_url"] == "/home/2/", response[1]["user_url"]
        assert response[0]["my_sub"] == True, response[0]["my_sub"]
        assert response[1]["my_sub"] == True, response[1]["my_sub"]


class TestSearchForGroupsMixin(TransactionTestCase):
    """Testing the SearchForGroupsMixin class methods"""

    fixtures = ["./config/tests/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.instance = types_of_search.SearchForGroupsMixin()
    
    async def test__search_for_groups(self):
        ### Searching groups that the user is own
        response = await self.instance._search_for_groups("group", 3)
        assert len(response) == 1, len(response)
        assert response[0]["name"] == "Second Group", response[0]["name"]
        assert response[0]["owner"] == 3, response[0]["owner"]
        assert len(response[0]["followers"]) == 1, len(response[0]["followers"])

        ### Searching groups that the user is follow
        response = await self.instance._search_for_groups("group", 1)
        assert len(response) == 2, len(response)
        assert response[0]["name"] == "My Group", response[0]["name"]
        assert response[0]["owner"] == 1, response[0]["owner"]
        assert len(response[0]["followers"]) == 0, len(response[0]["followers"])

        assert response[1]["name"] == "Second Group", response[1]["name"]
        assert response[1]["owner"] == 3, response[1]["owner"]
        assert len(response[1]["followers"]) == 1, len(response[1]["followers"])

        ### Nothing
        response = await self.instance._search_for_groups("grop", 1)
        assert len(response) == 0, len(response)

class TestGlobalSearchForGroupsMixin(TransactionTestCase):
    """Testing the GlobalSearchForGroupsMixin class methods"""

    fixtures = ["./config/tests/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.instance = types_of_search.GlobalSearchForGroupsMixin()
    
    async def test__search_for_global_groups(self):
        response = await self.instance._search_for_global_groups("group")
        assert len(response) == 2, len(response)
        assert response[0]["name"] == "My Group", response[0]["name"]
        assert response[0]["owner"] == 1, response[0]["owner"]
        assert len(response[0]["followers"]) == 0, len(response[0]["followers"])

        assert response[1]["name"] == "Second Group", response[1]["name"]
        assert response[1]["owner"] == 3, response[1]["owner"]
        assert len(response[1]["followers"]) == 1, len(response[1]["followers"])

        response = await self.instance._search_for_global_groups("my group")
        assert len(response) == 1, len(response)
        assert response[0]["name"] == "My Group", response[0]["name"]
        assert response[0]["owner"] == 1, response[0]["owner"]
        assert len(response[0]["followers"]) == 0, len(response[0]["followers"])

        response = await self.instance._search_for_global_groups("mygroup")
        assert len(response) == 0, len(response)