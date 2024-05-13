from .models import User


def get_user_or_none(username: str) -> User:
    """Get a user if he exists or return None"""

    try:
        return User.objects.get(username=username)
    except User.DoesNotExist:
        return None
