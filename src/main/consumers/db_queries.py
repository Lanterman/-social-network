import logging

from channels.db import database_sync_to_async

from src.users.models import Follower


@database_sync_to_async
def confirm_follower(follower_id: int, user_id: int) -> None:
    """Confirm follower"""

    Follower.objects.filter(follower_id__id=follower_id, subscription_id__id=user_id).update(is_checked=True)


@database_sync_to_async
def cancel_follower(follower_id: int, user_id: int) -> None:
    """Cancel follower"""

    Follower.objects.filter(follower_id__id=follower_id, subscription_id__id=user_id).delete()
