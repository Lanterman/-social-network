from django.test import TestCase


class TestConfirmFollowerMixin(TestCase):
    """Testing the ConfirmFollowerMixin class methods"""

    fixtures = ["./config/tests/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
    
    def test_conf_follower(self):
        pass


class TestChatMessageMixin(TestCase):
    """Testing the ChatMessageMixin class methods"""

    fixtures = ["./config/tests/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
    
    def test_get_sent_message(self):
        pass


class TestPublicationCommentMixin(TestCase):
    """Testing the PublicationCommentMixin class methods"""

    fixtures = ["./config/tests/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
    
    def test_get_comment_likes_dict(self):
        pass

    def test_add_or_remove_like(self):
        pass

    def test_comment_likes_activity(self):
        pass

    def test_get_comment(self):
        pass


class TestAllTypesOfSearchMixin(TestCase):
    """Testing the AllTypesOfSearchMixin class methods"""

    fixtures = ["./config/tests/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
    
    def test_search_for_publications(self):
        pass

    def test_search_for_messengers(self):
        pass

    def test_search_for_followers(self):
        pass

    def test_search_for_subscriptions(self):
        pass

    def test_search_for_global_users(self):
        pass

    def test_search_for_groups(self):
        pass

    def test_search_for_global_groups(self):
        pass