from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.backends import ModelBackend

from config import settings
from src.users.services import ValidateCustomPassword as ValidatePassword


UserModel = get_user_model()


class CustomAuthBackend(ModelBackend):
    """
    Custom authentication
    """

    keyword = settings.JWT_SETTINGS["AUTH_HEADER_TYPES"]

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)

        if username is None or password is None:
            return

        try:
            user = UserModel._default_manager.get_by_natural_key(username)
        except UserModel.DoesNotExist:
            return
        else:
            if user.is_staff:
                return user
            
            if self.user_can_authenticate(user) and ValidatePassword.validate_password(password, user.hashed_password):
                return user
