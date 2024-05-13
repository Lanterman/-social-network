from django.test import TransactionTestCase
from channels.db import database_sync_to_async

from src.main import models as main_models
from src.users import models as user_models
from src.main.consumers import db_queries


class TestGetUserByID(TransactionTestCase):
    """Testing the get_user_by_id function"""

    fixtures = ["./config/tests/test_data.json"]

    def setUp(self) -> None:
        super().setUp()
        self.instance = db_queries.get_user_by_id
    
    async def test_get_user_by_id(self):
        response = await self.instance(1)
        assert response.username == "admin", response.username

class TestConfirmFollower(TransactionTestCase):
    """Testing the confirm_follower function"""

    fixtures = ["./config/tests/test_data.json"]

    def setUp(self) -> None:
        super().setUp()
        self.instance = db_queries.confirm_follower
    
    @database_sync_to_async
    def check_instance(self, bool_value: bool) -> None:
        query = user_models.Follower.objects.get(id=2)
        assert query.is_checked == bool_value, query.is_checked

    async def test_confirm_follower(self):
        await self.check_instance(False)
        await self.instance(2, 3)
        await self.check_instance(True)


class TestCreateFollowerInstanceBySubID(TransactionTestCase):
    """Testing the create_follower_instance_by_sub_id function"""

    fixtures = ["./config/tests/test_data.json"]

    def setUp(self) -> None:
        super().setUp()
        self.instance = db_queries.create_follower_instance_by_sub_id
    
    @database_sync_to_async
    def check_count_instances(self, int_value: int) -> None:
        query = user_models.Follower.objects.count()
        assert query == int_value, query
    
    async def test_create_follower_instance_by_sub_id(self):
        await self.check_count_instances(3)
        await self.instance(2, 1)
        await self.check_count_instances(4)


class TestRemoveFollwoerInstances(TransactionTestCase):
    """Testing the remove_follower_instances function"""

    fixtures = ["./config/tests/test_data.json"]

    def setUp(self) -> None:
        super().setUp()
        self.instance = db_queries.remove_follower_instances
    
    @database_sync_to_async
    def check_count_instances(self, int_value: int) -> None:
        query = user_models.Follower.objects.count()
        assert query == int_value, query
    
    async def test_remove_follower_instances(self):
        await self.check_count_instances(3)
        await self.instance(2, 3)
        await self.check_count_instances(2)

        await self.check_count_instances(2)
        await self.instance(1, 3)
        await self.check_count_instances(0)


class TestRemoveFollowerInstanceByFollowerID(TransactionTestCase):
    """Testing the remove_follower_instance_by_follower_id function"""

    fixtures = ["./config/tests/test_data.json"]

    def setUp(self) -> None:
        super().setUp()
        self.instance = db_queries.remove_follower_instance_by_follower_id
    
    @database_sync_to_async
    def check_count_instances(self, int_value: int) -> None:
        query = user_models.Follower.objects.count()
        assert query == int_value, query
    
    async def test_remove_follower_instance_by_follower_id(self):
        await self.check_count_instances(3)
        await self.instance(1, 3)
        await self.check_count_instances(2)


class TestRemoveFollowerInstanceBySubID(TransactionTestCase):
    """Testing the remove_follower_instance_by_sub_id function"""

    fixtures = ["./config/tests/test_data.json"]

    def setUp(self) -> None:
        super().setUp()
        self.instance = db_queries.remove_follower_instance_by_sub_id
    
    @database_sync_to_async
    def check_count_instances(self, int_value: int) -> None:
        query = user_models.Follower.objects.count()
        assert query == int_value, query
    
    async def test_remove_follower_instance_by_sub_id(self):
        await self.check_count_instances(3)
        await self.instance(1, 3)
        await self.check_count_instances(2)


class TestGetPublicationUsingSearch(TransactionTestCase):
    """Testing the get_publications_using_search function"""

    fixtures = ["./config/tests/test_data.json"]

    def setUp(self) -> None:
        super().setUp()
        self.instance = db_queries.get_publications_using_search
    
    async def test_get_publications_using_search(self):
        response = await self.instance("publication")
        assert len(response) == 2, response
        assert response[0].rat == None, response[0].rat
        assert response[1].rat == None, response[1].rat
        assert response[0].owner.username == "admin", response[0].owner.username
        assert response[1].owner.username == "user", response[1].owner.username


class TestGetChatsUsingSearch(TransactionTestCase):
    """Testing the get_chats_using_search function"""

    fixtures = ["./config/tests/test_data.json"]

    def setUp(self) -> None:
        super().setUp()
        self.instance = db_queries.get_chats_using_search
    
    async def test_get_chats_using_search(self):
        response = await self.instance("qw", 1)
        assert len(response) == 2, response
        assert response[0].count_mes == 1, response[0].count_mes
        assert response[1].count_mes == 1, response[1].count_mes


class TestGetFollowersUsingSearch(TransactionTestCase):
    """Testing the get_followers_using_search function"""

    fixtures = ["./config/tests/test_data.json"]

    def setUp(self) -> None:
        super().setUp()
        self.instance = db_queries.get_followers_using_search
    
    async def test_get_followers_using_search(self):
        response = await self.instance("qw", 1)
        assert len(response) == 1, response
        assert response[0].follower_id.username == "lanterman", response[0].follower_id.username

        response = await self.instance("qw", 3)
        assert len(response) == 1, response
        assert response[0].follower_id.username == "user", response[0].follower_id.username

        response = await self.instance("", 3)
        assert len(response) == 2, response
        assert response[0].follower_id.username == "user", response[0].follower_id.username
        assert response[1].follower_id.username == "admin", response[1].follower_id.username


class TestGetSubsUsingSearch(TransactionTestCase):
    """Testing the get_subs_using_search function"""

    fixtures = ["./config/tests/test_data.json"]

    def setUp(self) -> None:
        super().setUp()
        self.instance = db_queries.get_subs_using_search
    
    async def test_get_subs_using_search(self):
        response = await self.instance("qw", 1)
        assert len(response) == 1, response
        assert response[0].subscription_id.username == "lanterman", response[0].subscription_id.username

        response = await self.instance("qw", 2)
        assert len(response) == 1, response
        assert response[0].subscription_id.username == "lanterman", response[0].subscription_id.username

        response = await self.instance("", 3)
        assert len(response) == 1, response
        assert response[0].subscription_id.username == "admin", response[0].subscription_id.username


class TestGetUsersUsingSearch(TransactionTestCase):
    """Testing the get_users_using_search function"""

    fixtures = ["./config/tests/test_data.json"]

    def setUp(self) -> None:
        super().setUp()
        self.instance = db_queries.get_users_using_search
    
    async def test_get_users_using_search(self):
        response = await self.instance("qw", 1)
        assert len(response) == 2, response
        assert response[0].username == "lanterman", response[0].username
        assert response[1].username == "user", response[1].username

        response = await self.instance("qw", 2)
        assert len(response) == 1, response
        assert response[0].username == "lanterman", response[0].username

        response = await self.instance("", 3)
        assert len(response) == 2, response
        assert response[0].username == "admin", response[0].username
        assert response[1].username == "user", response[1].username


class TestGetGroupsUsingSearch(TransactionTestCase):
    """Testing the get_groups_using_search function"""

    fixtures = ["./config/tests/test_data.json"]

    def setUp(self) -> None:
        super().setUp()
        self.instance = db_queries.get_groups_using_search
    
    async def test_get_groups_using_search(self):
        response = await self.instance("group", 1)
        assert len(response) == 2, response

        response = await self.instance("second group", 3)
        assert len(response) == 1, response
        assert response[0].name == "second group", response[0].name
        assert response[0].followers.count() == 1, response[0].followers.count()

        response = await self.instance("my group", 3)
        assert len(response) == 0, response


class TestGetGlobalGroupsUsingSearch(TransactionTestCase):
    """Testing the get_global_groups_using_search function"""

    fixtures = ["./config/tests/test_data.json"]

    def setUp(self) -> None:
        super().setUp()
        self.instance = db_queries.get_global_groups_using_search
    
    async def test_get_global_groups_using_search(self):
        response = await self.instance("group")
        assert len(response) == 2, response

        response = await self.instance("second group")
        assert len(response) == 1, response
        assert response[0].name == "second group", response[0].name
        assert response[0].followers.count() == 1, response[0].followers.count()

        response = await self.instance("my group")
        assert len(response) == 1, response


class TestCreatePubComment(TransactionTestCase):
    """Testing the create_pub_comment function"""

    fixtures = ["./config/tests/test_data.json"]

    def setUp(self) -> None:
        super().setUp()
        self.user = user_models.User.objects.get(id=1)
        self.instance = db_queries.create_pub_comment
    
    @database_sync_to_async
    def check_count_instances(self, int_value: int) -> None:
        query = main_models.Comment.objects.count()
        assert query == int_value, query
    
    async def test_create_pub_comment(self):
        await self.check_count_instances(2)
        await self.instance("comment", 1, self.user)
        await self.check_count_instances(3)


class TestGetPubCommentWithLikes(TransactionTestCase):
    """Testing the get_pub_comment_with_likes function"""

    fixtures = ["./config/tests/test_data.json"]

    def setUp(self) -> None:
        super().setUp()
        self.user = user_models.User.objects.get(id=1)
        self.comment = main_models.Comment.objects.get(id=1)
        self.instance = db_queries.get_pub_comment_with_likes
    
    @database_sync_to_async
    def add_like_to_comment(self, user: user_models.User) -> None:
        self.comment.like.add(user)
    
    async def test_get_pub_comment_with_likes(self):
        response = await self.instance(1)
        assert response.like.count() == 0, response.like.count()

        response = await self.instance(2)
        assert response.like.count() == 0, response.like.count()

        await self.add_like_to_comment(self.user)
        response = await self.instance(1)
        assert response.like.count() == 1, response.like.count()
