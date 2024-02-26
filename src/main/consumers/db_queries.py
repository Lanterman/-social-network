import logging

from django.db.models import Q
from channels.db import database_sync_to_async

from src.users.models import Follower


@database_sync_to_async
def confirm_follower(follower_id: int, user_id: int) -> None:
    """Confirm follower"""

    Follower.objects.filter(follower_id__id=follower_id, subscription_id__id=user_id).update(is_checked=True)


@database_sync_to_async
def create_follower_instance_by_sub_id(subscription_id: int, user_id: int) -> None:
    """Create follower instance by subscription id"""

    Follower.objects.create(follower_id_id=user_id, subscription_id_id=subscription_id)


@database_sync_to_async
def remove_follower_instance_by_follower_id(follower_id: int, user_id: int) -> None:
    """Remove follower instance by follower id"""

    Follower.objects.filter(follower_id__id=follower_id, subscription_id__id=user_id).delete()


@database_sync_to_async
def remove_follower_instance_by_sub_id(subscription_id: int, user_id: int) -> None:
    """Remove follower instance by subscription id"""

    Follower.objects.filter(follower_id__id=user_id, subscription_id__id=subscription_id).delete()


@database_sync_to_async
def subs_search(search_value: str, user_id: int) -> tuple:
    """Subscriptions search"""

    query = Follower.objects.filter(
            Q(subscription_id__username__icontains=search_value, follower_id__id=user_id) |
            Q(subscription_id__first_name__icontains=search_value, follower_id__id=user_id) |
            Q(subscription_id__last_name__icontains=search_value, follower_id__id=user_id)
        ).select_related("subscription_id")
    
    return list(query), "qwe"