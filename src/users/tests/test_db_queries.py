from django.test import TestCase

from src.users import db_queries


class GetUserOrNoneTest(TestCase):
    """Testing the get_user_or_none function"""

    fixtures = ["./config/tests/test_data.json"]

    def test_get_user(self):
        user = db_queries.get_user_or_none("lanterman")
        assert user.id == 3, user.id
    
    def test_get_none(self):
        response = db_queries.get_user_or_none("qwer")
        assert response is None, response