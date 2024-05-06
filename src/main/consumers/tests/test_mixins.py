from django.test import TestCase, TransactionTestCase


from src.main.consumers import mixins, serializers
from src.main import models as main_models
from src.users import models as user_models


class TestConfirmFollowerMixin(TransactionTestCase):
    """Testing the ConfirmFollowerMixin class methods"""

    fixtures = ["./config/tests/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.instance = mixins.ConfirmFollowerMixin()
    
    async def test_conf_follower(self):
        response = await self.instance.conf_follower(1)
        assert response["id"] == 1, response["id"]
        assert response["user_full_name"] == "Anonymous", response["user_full_name"]
        assert response["user_url"] == "/home/1/", response["user_url"]

        response = await self.instance.conf_follower(3)
        assert response["id"] == 3, response["id"]
        assert response["user_full_name"] == "Qweqweqwe Qweqweqe", response["user_full_name"]
        assert response["user_url"] == "/home/3/", response["user_url"]


class TestChatMessageMixin(TestCase):
    """Testing the ChatMessageMixin class methods"""

    fixtures = ["./config/tests/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = user_models.User.objects.get(id=3)
        cls.instance = mixins.ChatMessageMixin()
    
    def test_get_sent_message(self):
        response = self.instance.get_sent_message("Hi man!", self.user)
        assert response["message"] == "Hi man!", response["message"]
        assert response["author"]["name"] == "qweqweqwe qweqweqe", response["author"]["name"]
        assert response["author"]["url"] == "/home/3/", response["author"]["url"]

        response = self.instance.get_sent_message("Hi man! \n How are you?", self.user)
        assert response["message"] == "Hi man! </br> How are you?", response["message"]
        assert response["author"]["name"] == "qweqweqwe qweqweqe", response["author"]["name"]
        assert response["author"]["url"] == "/home/3/", response["author"]["url"]


class TestPublicationCommentMixin(TransactionTestCase):
    """Testing the PublicationCommentMixin class methods"""

    fixtures = ["./config/tests/test_data.json"]

    def setUp(self) -> None:
        super().setUp()
        self.user_1 = user_models.User.objects.get(id=2)
        self.user_2 = user_models.User.objects.get(id=3)
        self.comment = main_models.Comment.objects.get(id=1)
        self.instance = mixins.PublicationCommentMixin()
    
    async def test_get_comment_likes_dict(self):
        response = await self.instance.get_comment_likes_dict(self.comment, {"like_from_me": 0})
        assert response == {"like_from_me": 0, "comment_id": 1, "likes_count": 0}

        response = await self.instance.get_comment_likes_dict(self.comment, {"like_from_me": 1})
        assert response == {"like_from_me": 1, "comment_id": 1, "likes_count": 0}

    async def test_add_or_remove_like(self):
        response = await self.instance.add_or_remove_like(self.comment, self.user_2)
        assert response == {"like_from_me": 1}, response

        response = await self.instance.add_or_remove_like(self.comment, self.user_1)
        assert response == {"like_from_me": 1}, response

        response = await self.instance.add_or_remove_like(self.comment, self.user_2)
        assert response == {"like_from_me": 0}, response

    async def test_comment_likes_activity(self):
        response = await self.instance.comment_likes_activity(self.comment.id, self.user_1)
        assert response == {"like_from_me": 1, "comment_id": 1, "likes_count": 1}

        response = await self.instance.comment_likes_activity(self.comment.id, self.user_2)
        assert response == {"like_from_me": 1, "comment_id": 1, "likes_count": 2}

        response = await self.instance.comment_likes_activity(self.comment.id, self.user_1)
        assert response == {"like_from_me": 0, "comment_id": 1, "likes_count": 1}

    async def test_get_comment(self):
        response = await self.instance.get_comment("It's the good comment!", 1, self.user_1)
        assert response["biography"] == "It's the good comment!", response["biography"]
        assert response["users"]["url"] == "/home/2/", response["users"]["url"]
        assert response["users"]["username"] == "user", response["users"]["username"]

        response = await self.instance.get_comment("It's the <i>good</i> comment!", 1, self.user_2)
        assert response["biography"] == "It's the <i>good</i> comment!", response["biography"]
        assert response["users"]["url"] == "/home/3/", response["users"]["url"]
        assert response["users"]["username"] == "lanterman", response["users"]["username"]


class TestAllTypesOfSearchMixin(TransactionTestCase):
    """Testing the AllTypesOfSearchMixin class methods"""

    fixtures = ["./config/tests/test_data.json"]

    def setUp(self) -> None:
        super().setUp()
        self.instance = mixins.AllTypesOfSearchMixin()
        self.user_1 = user_models.User.objects.get(id=1)
        self.user_2 = user_models.User.objects.get(id=2)
        self.user_3 = user_models.User.objects.get(id=3)

        self.user_ser_1 = serializers.UserSearchSerialazer(self.user_1).data
        self.user_ser_2 = serializers.UserSearchSerialazer(self.user_2).data
        self.user_ser_3 = serializers.UserSearchSerialazer(self.user_3).data
    
    async def test_search_for_publications(self):
        ### searching for by the name field the owner field
        response = await self.instance.search_for_publications("admin")
        assert len(response) == 1, len(response)
        assert response[0]["name"] == "Publication", response[0]["name"]
        assert response[0]["owner"]["username"] == "admin", response[0]["owner"]["username"]

        ### searching for by the name field
        response = await self.instance.search_for_publications("second")
        assert len(response) == 1, len(response)
        assert response[0]["name"] == "Second Publication", response[0]["name"]
        assert response[0]["owner"]["username"] == "user", response[0]["owner"]["username"]

        response = await self.instance.search_for_publications("secodn")
        assert len(response) == 0, len(response)

    async def test_search_for_messengers(self):
        ### searching for by the first_name field
        response = await self.instance.search_for_messengers("qwe", 1)
        assert len(response) == 2, len(response)
        assert response[0]["id"] == 1, response[0]["id"]
        assert len(response[0]["message_set"]) == 1, len(response[0]["message_set"])
        assert response[0]["members"][0]["user_url"] == "/home/2/", response[0]["members"][0]["user_url"]

        ### searching for by the last_name field
        response = await self.instance.search_for_messengers("qwe", 3)
        assert len(response) == 1, len(response)
        assert response[0]["id"] == 2, response[0]["id"]
        assert len(response[0]["message_set"]) == 1, len(response[0]["message_set"])
        assert response[0]["members"][0]["user_url"] == "/home/1/", response[0]["members"][0]["user_url"]

        response = await self.instance.search_for_messengers("qqwe", 3)
        assert len(response) == 0, response

    async def test_search_for_followers(self):
        response = await self.instance.search_for_followers("lanterm", 1)
        assert len(response) == 1, len(response)
        assert response[0]["id"] == 3, response[0]["id"]
        assert response[0]["user_url"] == "/home/3/", response[0]["user_url"]

        response = await self.instance.search_for_followers("r", 1)
        assert len(response) == 1, len(response)
        assert response[0]["id"] == 3, response[0]["id"]
        assert response[0]["user_url"] == "/home/3/", response[0]["user_url"]

        response = await self.instance.search_for_followers("lanterman", 2)
        assert len(response) == 0, len(response)

        response = await self.instance.search_for_followers("user", 1)
        assert len(response) == 0, len(response)

    async def test_search_for_subscriptions(self):
        response = await self.instance.search_for_subscriptions("admin", 3)
        assert len(response) == 1, len(response)
        assert response[0]["id"] == 1, response[0]["id"]
        assert response[0]["user_url"] == "/home/1/", response[0]["user_url"]

        response = await self.instance.search_for_subscriptions("r", 1)
        assert len(response) == 1, len(response)
        assert response[0]["id"] == 3, response[0]["id"]
        assert response[0]["user_url"] == "/home/3/", response[0]["user_url"]

        response = await self.instance.search_for_subscriptions("user", 3)
        assert len(response) == 0, len(response)

        response = await self.instance.search_for_subscriptions("admin", 2)
        assert len(response) == 0, len(response)

    async def test_search_for_global_users(self):
        response = await self.instance.search_for_global_users(
            "r", self.user_1.id, [self.user_ser_2], [self.user_ser_3, self.user_ser_2]
        )
        assert len(response) == 2, len(response)
        assert response[0]["id"] == 3, response[0]["id"]
        assert response[1]["id"] == 2, response[1]["id"]
        assert response[1]["user_url"] == "/home/2/", response[1]["user_url"]
        assert response[0]["my_follower"] == True, response[0]["my_follower"]
        assert response[1]["my_follower"] == True, response[1]["my_follower"]
        assert response[1]["my_sub"] == True, response[1]["my_sub"]

        response = await self.instance.search_for_global_users("r", self.user_1.id, [self.user_ser_3, self.user_ser_2], [])
        assert len(response) == 2, len(response)
        assert response[0]["id"] == 3, response[0]["id"]
        assert response[1]["id"] == 2, response[1]["id"]
        assert response[1]["user_url"] == "/home/2/", response[1]["user_url"]
        assert response[0]["my_sub"] == True, response[0]["my_sub"]
        assert response[1]["my_sub"] == True, response[1]["my_sub"]

    async def test_search_for_groups(self):
        ### Searching groups that the user is own
        response = await self.instance.search_for_groups("group", 3)
        assert len(response) == 1, len(response)
        assert response[0]["name"] == "Second Group", response[0]["name"]
        assert response[0]["owner"] == 3, response[0]["owner"]
        assert len(response[0]["followers"]) == 1, len(response[0]["followers"])

        ### Searching groups that the user is follow
        response = await self.instance.search_for_groups("group", 1)
        assert len(response) == 2, len(response)
        assert response[0]["name"] == "My Group", response[0]["name"]
        assert response[0]["owner"] == 1, response[0]["owner"]
        assert len(response[0]["followers"]) == 0, len(response[0]["followers"])

        assert response[1]["name"] == "Second Group", response[1]["name"]
        assert response[1]["owner"] == 3, response[1]["owner"]
        assert len(response[1]["followers"]) == 1, len(response[1]["followers"])

        ### Nothing
        response = await self.instance.search_for_groups("grop", 1)
        assert len(response) == 0, len(response)

    async def test_search_for_global_groups(self):
        response = await self.instance.search_for_global_groups("group")
        assert len(response) == 2, len(response)
        assert response[0]["name"] == "My Group", response[0]["name"]
        assert response[0]["owner"] == 1, response[0]["owner"]
        assert len(response[0]["followers"]) == 0, len(response[0]["followers"])

        assert response[1]["name"] == "Second Group", response[1]["name"]
        assert response[1]["owner"] == 3, response[1]["owner"]
        assert len(response[1]["followers"]) == 1, len(response[1]["followers"])

        response = await self.instance.search_for_global_groups("my group")
        assert len(response) == 1, len(response)
        assert response[0]["name"] == "My Group", response[0]["name"]
        assert response[0]["owner"] == 1, response[0]["owner"]
        assert len(response[0]["followers"]) == 0, len(response[0]["followers"])

        response = await self.instance.search_for_global_groups("mygroup")
        assert len(response) == 0, len(response)