from datetime import datetime
from django.test import TestCase

from src.main.models import Publication, Group, Comment
from src.users.models import User, Chat, Message, Follower
from src.main.consumers import serializers


class TestFormattingClass(TestCase):
    """Testing the FormattingClass class methods"""

    fixtures = ["./config/tests/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.instance = serializers.FormattingClass()
    
    def test_get_short_field_value(self):
        response = self.instance.get_short_field_value("shortname")
        assert response == "shortname", response

        response = self.instance.get_short_field_value("longername1")
        assert response == "longername...", response

        response = self.instance.get_short_field_value("shortname", 12)
        assert response == "shortname", response

        response = self.instance.get_short_field_value("longername123", 12)
        assert response == "longername12...", response

    def test_get_formatted_date(self):
        response = self.instance.get_formatted_date(datetime(2024, 12, 1))
        assert response == "01.12.2024, 00:00:00", response

        response = self.instance.get_formatted_date(datetime(2024, 12, 1, 5))
        assert response == "01.12.2024, 05:00:00", response

    def test_get_formatted_user_full_name(self):
        response = self.instance.get_formatted_user_full_name("")
        assert response == "Anonymous", response

        response = self.instance.get_formatted_user_full_name("my name")
        assert response == "My Name", response

        response = self.instance.get_formatted_user_full_name("qweqweqweqweq eqweqweqweqwe")
        assert response == "Qweqweqweqweq Eqweqw...", response

        response = self.instance.get_formatted_user_full_name("my name", 10)
        assert response == "My Name", response

        response = self.instance.get_formatted_user_full_name("qweqweqweqweq eqweqweqweqwe", 18)
        assert response == "Qweqweqweqweq Eqwe...", response


class TestUserForPublication(TestCase):
    """Testing the UserForPublication class methods"""

    fixtures = ["./config/tests/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = User.objects.get(id=3)
        cls.instance = serializers.UserForPublication
    
    def test_to_representation(self):
        response = self.instance(self.user).data
        assert response["username"] == "lanterman", response["username"]
        assert response["user_url"] == "/home/3/", response["user_url"]

        self.user.id = 11
        self.user.username = "lantermanisbest"
        response = self.instance(self.user).data
        assert response["username"] == "lantermani...", response["username"]
        assert response["user_url"] == "/home/11/", response["user_url"]


class TestUserForCommentOfPub(TestCase):
    """Testing the UserForCommentOfPub class methods"""

    fixtures = ["./config/tests/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = User.objects.get(id=3)
        cls.instance = serializers.UserForCommentOfPub
    
    def test_to_representation(self):
        response = self.instance(self.user).data
        assert response["username"] == "lanterman", response["username"]
        assert response["url"] == "/home/3/", response["url"]

        self.user.id = 11
        self.user.username = "lantermanisbest" * 14
        response = self.instance(self.user).data
        assert response["username"] == f"{'lantermanisbest' * 13}lante...", response["username"]
        assert response["url"] == "/home/11/", response["url"]


class TestMemberForChatSerialazer(TestCase):
    """Testing the MemberForChatSerialazer class methods"""

    fixtures = ["./config/tests/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = User.objects.get(id=3)
        cls.instance = serializers.MemberForChatSerialazer
    
    def test_to_representation(self):
        response = self.instance(self.user).data
        assert response["user_full_name"] == "Qweqweqwe Qweqweqe", response["user_full_name"]
        assert response["user_url"] == "/home/3/", response["user_url"]

        self.user.id = 11
        self.user.first_name = "lanterman" * 4
        response = self.instance(self.user).data
        assert response["user_full_name"] == f"{('lanterman' * 4).title()} Qwe...", response["user_full_name"]
        assert response["user_url"] == "/home/11/", response["user_url"]


class TestAuthorForChatMessageSerialazer(TestCase):
    """Testing the AuthorForChatMessageSerialazer class methods"""

    fixtures = ["./config/tests/test_data.json"]

    def setUp(cls) -> None:
        super().setUp()
        cls.user_1 = User.objects.get(id=1)
        cls.user_2 = User.objects.get(id=3)
        cls.instance = serializers.AuthorForChatMessageSerialazer
    
    def test_get_author_name(self):
        ### It ha the full name
        response = self.instance.get_author_name(self.user_2)
        assert response == "qweqweqwe qweqweqe", response

        self.user_2.first_name = "lanterman" * 5
        response = self.instance.get_author_name(self.user_2)
        assert response == f"{('lanterman' * 5)} qweq...", response

        ### It hasn't the full name
        response = self.instance.get_author_name(self.user_1)
        assert response == "admin", response

        self.user_1.username = "admin1" * 9
        response = self.instance.get_author_name(self.user_1)
        assert response == f"{'admin1' * 8}ad...", response

    def test_to_representation(self):
        ### It ha the full name
        response = self.instance(self.user_2).data
        assert response["name"] == "qweqweqwe qweqweqe", response["name"]
        assert response["url"] == "/home/3/", response["url"]

        self.user_2.id = 11
        self.user_2.first_name = "lanterman" * 5
        response = self.instance(self.user_2).data
        assert response["name"] == f"{('lanterman' * 5)} qweq...", response["name"]
        assert response["url"] == "/home/11/", response["url"]

        ### It hasn't the full name
        response = self.instance(self.user_1).data
        assert response["name"] == "admin", response["name"]
        assert response["url"] == "/home/1/", response["url"]

        self.user_1.id = 11
        self.user_1.username = "admin1" * 9
        response = self.instance(self.user_1).data
        assert response["name"] == f"{'admin1' * 8}ad...", response["name"]
        assert response["url"] == "/home/11/", response["url"]


class TestLastChatMessage(TestCase):
    """Testing the LastChatMessage class methods"""

    fixtures = ["./config/tests/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.message_1 = Message.objects.get(id=1)
        cls.message_2 = Message.objects.get(id=2)
        cls.instance = serializers.LastChatMessage
    
    def test_to_representation(self):
        response = self.instance(self.message_1).data
        assert response["pub_date"] == "14.04.2024, 09:27:29", response["pub_date"]

        response = self.instance(self.message_2).data
        assert response["pub_date"] == "14.04.2024, 09:27:40", response["pub_date"]


class TestConfirmFollowerSerialazer(TestCase):
    """Testing the ConfirmFollowerSerialazer class methods"""

    fixtures = ["./config/tests/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user_1 = User.objects.get(id=1)
        cls.user_2 = User.objects.get(id=3)
        cls.instance = serializers.ConfirmFollowerSerialazer
    
    def test_to_representation(self):
        response = self.instance(self.user_1).data
        assert response["user_full_name"] == "Anonymous", response["user_full_name"]
        assert response["user_url"] == "/home/1/", response["user_url"]

        self.user_1.id = 12
        self.user_1.first_name = "lanterma" * 2
        response = self.instance(self.user_1).data
        assert response["user_full_name"] == ('lanterma' * 2).title(), response["user_full_name"]
        assert response["user_url"] == "/home/12/", response["user_url"]

        self.user_1.last_name = "admin"
        response = self.instance(self.user_1).data
        assert response["user_full_name"] == f"{('lanterma' * 2).title()} Adm...", response["user_full_name"]

        response = self.instance(self.user_2).data
        assert response["user_full_name"] == "Qweqweqwe Qweqweqe", response["user_full_name"]
        assert response["user_url"] == "/home/3/", response["user_url"]

        self.user_2.id = 11
        self.user_2.first_name = "lanterman" * 2
        response = self.instance(self.user_2).data
        assert response["user_full_name"] == f"{('lanterman' * 2).title()} Q...", response["user_full_name"]
        assert response["user_url"] == "/home/11/", response["user_url"]


class TestCommentOfPublicationSerializer(TestCase):
    """Testing the CommentOfPublicationSerializer class methods"""

    fixtures = ["./config/tests/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.comment = Comment.objects.get(id=1)
        cls.instance = serializers.CommentOfPublicationSerializer
    
    def test_to_representation(self):
        response = self.instance(self.comment).data
        assert response["id"] == 1, response["id"]
        assert response["biography"] == "Good Question!", response["biography"]
        assert response["users"]["id"] == 1, response["users"]["id"]
        assert response["users"]["username"] == "admin", response["users"]["username"]
        assert response["users"]["url"] == "/home/1/", response["users"]["url"]


class TestPublicationSearchSerialazer(TestCase):
    """Testing the PublicationSearchSerialazer class methods"""

    fixtures = ["./config/tests/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.publication = Publication.objects.get(id=1)
        cls.instance = serializers.PublicationSearchSerialazer
        cls.publication.rat = 3
    
    def test_get_formatted_biography(self):
        response = self.instance.get_formatted_biography("My biography")
        assert response == "My biography", response

        response = self.instance.get_formatted_biography("My biography", 10)
        assert response == "My biograp...", response

        response = self.instance.get_formatted_biography("My biography \n Yep!")
        assert response == "My biography </br> Yep!", response

        response = self.instance.get_formatted_biography("My biography \n Yep!", 17)
        assert response == "My biography </br...", response
    
    def test_to_representation(self):
        biography = "It's my first publication. Nothing intresting. Just the publication."
        response = self.instance(self.publication).data
        assert response["name"] == "Publication", response["name"]
        assert response["biography"] == biography, response["biography"]
        assert response["date"] == "14.04.2024, 09:26:22", response["date"]
        assert response["rating"] == 3, response["rating"]
        assert response["publication_url"] == "/publish/publication/", response["publication_url"]

        self.publication.name = "publication " * 3
        self.publication.biography = "My biography \n Yep!"
        self.publication.date = datetime(2024, 12, 1)
        self.publication.rat = 4
        self.publication.slug = "slugpiub"
        response = self.instance(self.publication).data
        assert response["name"] == f"{'Publication ' * 2}Public...", response["name"]
        assert response["biography"] == "My biography </br> Yep!", response["biography"]
        assert response["date"] == "01.12.2024, 00:00:00", response["date"]
        assert response["rating"] == 4, response["rating"]
        assert response["publication_url"] == "/publish/slugpiub/", response["publication_url"]


class TestChatSearchSerialaizer(TestCase):
    """Testing the ChatSearchSerialazer class methods"""

    fixtures = ["./config/tests/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.chat = Chat.objects.prefetch_related("members", "message_set").get(id=1)
        cls.instance = serializers.ChatSearchSerialazer
    
    def test_get_formatted_last_message(self):
        message_dict = {"message": "my message"}
        response = self.instance.get_formatted_last_message(message_dict)
        assert response == {"message": "my message"}, response

        response = self.instance.get_formatted_last_message(message_dict, 6)
        assert response == {"message": "my mes..."}, response

        message_dict = {"message": "my <i>message</i>"}
        response = self.instance.get_formatted_last_message(message_dict.copy())
        assert response == {"message": "my < i>message< /i>"}, response

        response = self.instance.get_formatted_last_message(message_dict.copy(), 10)
        assert response == {"message": "my < i>mes..."}, response

    def test_to_representation(self):
        response = self.instance(self.chat).data
        assert response["chat_url"] == "/chat/1/", response["chat_url"]
        assert response["last_message"]["message"] == "Hi man", response["last_message"]["message"]


class TestUserSearchSerialazer(TestCase):
    """Testing the UserSearchSerialazer class methods"""

    fixtures = ["./config/tests/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = User.objects.get(id=3)
        cls.instance = serializers.UserSearchSerialazer
    
    def test_to_representation(self):
        response = self.instance(self.user).data
        assert response["user_full_name"] == "qweqweqwe qweqweqe", response["user_full_name"]
        assert response["user_url"] == "/home/3/", response["user_url"]


class TestFollowerSearchSerialazer(TestCase):
    """Testing the FollowerSearchSerialazer class methods"""

    fixtures = ["./config/tests/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = Follower.objects.prefetch_related("follower_id").get(id=2)
        cls.instance = serializers.FollowerSearchSerialazer
    
    def test_to_representation(self):
        response = self.instance(self.user).data
        assert response["user_full_name"] == "qweqweqwe qweqweqwe", response["user_full_name"]
        assert response["user_url"] == "/home/2/", response["user_url"]


class TestSubscriptionsSearchSerialazer(TestCase):
    """Testing the SubscriptionsSearchSerialazer class methods"""

    fixtures = ["./config/tests/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = Follower.objects.prefetch_related("subscription_id").get(id=2)
        cls.instance = serializers.SubscriptionsSearchSerialazer
    
    def test_to_representation(self):
        response = self.instance(self.user).data
        assert response["user_full_name"] == "qweqweqwe qweqweqe", response["user_full_name"]
        assert response["user_url"] == "/home/3/", response["user_url"]


class TestGroupsSearchSerialazer(TestCase):
    """Testing the GroupsSearchSerialazer class methods"""

    fixtures = ["./config/tests/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.group = Group.objects.get(id=1)
        cls.instance = serializers.GroupsSearchSerialazer
    
    def test_to_representation(self):
        response = self.instance(self.group).data
        assert response["owner"] == 1, response["owner"]
        assert response["group_url"] == "/groups/my_group/", response["group_url"]

        self.group.slug = "slug_group"
        response = self.instance(self.group).data
        assert response["owner"] == 1, response["owner"]
        assert response["group_url"] == "/groups/slug_group/", response["group_url"]
