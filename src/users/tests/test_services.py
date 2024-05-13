import pytest

from django.test import RequestFactory, TestCase
from django.urls import reverse

from src.users import services, models, form as user_forms


class TestCreateSalt:
    """Testing the create_salt function"""

    @pytest.mark.parametrize("input_data, output_data", [(None, 12), (10, 10), (100, 100)])
    def test_create_salt(self, input_data: str, output_data: str):
        if input_data:
            response = services.create_salt(input_data)
        else:
            response = services.create_salt()
        
        assert len(response) == output_data, len(response)
        assert type(response) == str, type(response)


class TestPasswordHashing:
    """Testing the password_hashing function"""

    @pytest.mark.parametrize(
            "input_data, output_data", 
            [(("qweqweq", "qqqq"), str), (("qweqweq", "qqqq"), str), (("qweqweq", None), str)]
    )
    def test_password_hashing(self, input_data: str, output_data: str):
        response = services.password_hashing(*input_data)
        assert type(response) == output_data, type(response)


class TestCreateHashedPassword:
    """Testing the create_hashed_password function"""

    @pytest.mark.parametrize(
            "input_data, output_data", 
            [("qweqweq", str), ("qweqweqq", str), ("qwe1qweq", str)]
    )
    def test_create_hashed_password(self, input_data: str, output_data: str):
        response = services.create_hashed_password(input_data)
        assert "$" in response, response
        assert type(response) == output_data, type(response)
        assert len(response[:response.index("$")]), len(response[:response.index("$")])


class TestValidateCustomPasswordByPytest:
    """Testing the ValidateCustomPassword class"""

    @pytest.fixture(autouse=True)
    def instance(self):
        _instance = services.ValidateCustomPassword()
        return _instance
    
    @pytest.mark.parametrize(
            "input_data, output_data", 
            [
                (("karmavdel", "JBaLpBqMzIda$bd0d35ed587d7b86f943a82efe559c94264009177c831be7afb7286de4eff373"), False), 
                (("karmavdele", "JBaLpBqMzIda$bd0d35ed587d7b86f943a82efe559c94264009177c831be7afb7286de4eff473"), False)
            ]
    )
    def test_validate_password__invalid(self, input_data: str, output_data: str, instance: services.ValidateCustomPassword):
        response = instance.validate_password(*input_data)
        assert response == output_data, response
    
    @pytest.mark.parametrize(
            "input_data, output_data", 
            [
                (("karmavdele", "JBaLpBqMzIda$bd0d35ed587d7b86f943a82efe559c94264009177c831be7afb7286de4eff373"), True), 
                (("karmavdele", "wZIgZAtZEKls$41772c6250665d9bcbabc7c48d2415f6c21797d61811940fd1c9c136711630da"), True)
            ]
    )
    def test_validate_password__valid(self, input_data: str, output_data: str, instance: services.ValidateCustomPassword):
        response = instance.validate_password(*input_data)
        assert response == output_data, response


class TestValidateCustomPasswordByUnittest(TestCase):
    """Testing the ValidateCustomPassword class"""

    fixtures = ["./config/tests/test_data.json"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = models.User.objects.get(id=3)
        cls.request_obj = RequestFactory()
        cls.url = reverse("login")

        cls.valid_user_data = {"username": "lanterman", "password": "karmavdele"}
        cls.invalid_user_data_1 = {"username": "lanerman", "password": "karmavdele"}
        cls.invalid_user_data_2 = {"username": "lanterman", "password": "karmavdel"}

    def test_valid_check_custom_password(self):
        """Testing the valid check_custom_password method"""

        request = self.request_obj.post(self.url, data=self.valid_user_data)
        form = user_forms.LoginUserForm(request, request.POST)
        services.ValidateCustomPassword().check_custom_password("password", self.user, form)
        self.assertFalse(form.errors, form.errors)
    
    def test_invalid_check_custom_password_by_incorrect_username(self):
        """Testing the invalid check_custom_password method by incorrect username"""

        request = self.request_obj.post(self.url, data=self.invalid_user_data_1)
        form = user_forms.LoginUserForm(request, request.POST)
        services.ValidateCustomPassword().check_custom_password("password", self.user, form)
        assert form.errors, form.errors
        assert len(form.errors) == 1, form.errors
    
    def test_invalid_check_custom_password_by_incorrect_password(self):
        """Testing the invalid check_custom_password method by incorrect password"""

        request = self.request_obj.post(self.url, data=self.invalid_user_data_2)
        form = user_forms.LoginUserForm(request, request.POST)
        services.ValidateCustomPassword().check_custom_password("password", self.user, form)
        assert form.errors, form.errors
        assert len(form.errors) == 1, form.errors
