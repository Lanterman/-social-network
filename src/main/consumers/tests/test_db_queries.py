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
        pass


class TestGetChatsUsingSearch(TransactionTestCase):
    """Testing the get_chats_using_search function"""

    fixtures = ["./config/tests/test_data.json"]

    def setUp(self) -> None:
        super().setUp()
        self.instance = db_queries.get_chats_using_search
    
    async def test_get_chats_using_search(self):
        pass


class TestGetFollowersUsingSearch(TransactionTestCase):
    """Testing the get_followers_using_search function"""

    fixtures = ["./config/tests/test_data.json"]

    def setUp(self) -> None:
        super().setUp()
        self.instance = db_queries.get_followers_using_search
    
    async def test_get_followers_using_search(self):
        pass


class TestGetSubsUsingSearch(TransactionTestCase):
    """Testing the get_subs_using_search function"""

    fixtures = ["./config/tests/test_data.json"]

    def setUp(self) -> None:
        super().setUp()
        self.instance = db_queries.get_subs_using_search
    
    async def test_get_subs_using_search(self):
        pass


class TestGetUsersUsingSearch(TransactionTestCase):
    """Testing the get_users_using_search function"""

    fixtures = ["./config/tests/test_data.json"]

    def setUp(self) -> None:
        super().setUp()
        self.instance = db_queries.get_users_using_search
    
    async def test_get_users_using_search(self):
        pass


class TestGetGroupsUsingSearch(TransactionTestCase):
    """Testing the get_groups_using_search function"""

    fixtures = ["./config/tests/test_data.json"]

    def setUp(self) -> None:
        super().setUp()
        self.instance = db_queries.get_groups_using_search
    
    async def test_get_groups_using_search(self):
        pass


class TestGetGlobalGroupsUsingSearch(TransactionTestCase):
    """Testing the get_global_groups_using_search function"""

    fixtures = ["./config/tests/test_data.json"]

    def setUp(self) -> None:
        super().setUp()
        self.instance = db_queries.get_global_groups_using_search
    
    async def test_get_global_groups_using_search(self):
        pass


class TestCreatePubComment(TransactionTestCase):
    """Testing the create_pub_comment function"""

    fixtures = ["./config/tests/test_data.json"]

    def setUp(self) -> None:
        super().setUp()
        self.instance = db_queries.create_pub_comment
    
    async def test_create_pub_comment(self):
        pass


class TestGetPubCommentWithLikes(TransactionTestCase):
    """Testing the get_pub_comment_with_likes function"""

    fixtures = ["./config/tests/test_data.json"]

    def setUp(self) -> None:
        super().setUp()
        self.instance = db_queries.get_pub_comment_with_likes
    
    async def test_get_pub_comment_with_likes(self):
        pass