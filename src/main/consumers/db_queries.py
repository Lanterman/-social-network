import logging

from django.db.models import Q, Avg
from channels.db import database_sync_to_async

from src.users.models import Follower, User
from src.main.models import Publication, Group


@database_sync_to_async
def get_user_by_id(user_id: int) -> User:
    """Get a user by id"""

    return User.objects.get(id=user_id)


# Follower activity
@database_sync_to_async
def confirm_follower(follower_id: int, user_id: int) -> None:
    """Confirm follower"""

    Follower.objects.filter(follower_id__id=follower_id, subscription_id__id=user_id).update(is_checked=True)


@database_sync_to_async
def create_follower_instance_by_sub_id(subscription_id: int, user_id: int) -> None:
    """Create follower instance by subscription id"""

    Follower.objects.create(follower_id_id=user_id, subscription_id_id=subscription_id)


@database_sync_to_async
def remove_follower_instances(follower_id: int, user_id: int) -> None:
    """Remove instances where user's a subscriber and user's a follower"""

    Follower.objects.filter(
        Q(follower_id__id=follower_id, subscription_id__id=user_id) |
        Q(follower_id__id=user_id, subscription_id__id=follower_id)                  
    ).delete()


@database_sync_to_async
def remove_follower_instance_by_follower_id(follower_id: int, user_id: int) -> None:
    """Remove follower instance by follower id"""

    Follower.objects.filter(follower_id__id=follower_id, subscription_id__id=user_id).delete()


@database_sync_to_async
def remove_follower_instance_by_sub_id(subscription_id: int, user_id: int) -> None:
    """Remove follower instance by subscription id"""

    Follower.objects.filter(follower_id__id=user_id, subscription_id__id=subscription_id).delete()


# All types of search
@database_sync_to_async
def get_publications_by_search(search_value: str) -> list:
    """Get publications by search"""

    query = Publication.objects.filter(
            Q(name__icontains=search_value) | Q(owner__username__icontains=search_value)
        ).select_related('owner').annotate(rat=Avg('rating__star_id'))
    
    return list(query)    


@database_sync_to_async
def get_followers_search(search_value: str, user_id: int) -> list:
    """Get followers by search"""

    query = Follower.objects.filter(
            Q(follower_id__username__icontains=search_value, subscription_id__id=user_id) |
            Q(follower_id__first_name__icontains=search_value, subscription_id__id=user_id) |
            Q(follower_id__last_name__icontains=search_value, subscription_id__id=user_id)
        ).select_related("follower_id")
    
    return list(query)


@database_sync_to_async
def get_subs_search(search_value: str, user_id: int) -> list:
    """Get subscriptions by search"""

    query = Follower.objects.filter(
            Q(subscription_id__username__icontains=search_value, follower_id__id=user_id) |
            Q(subscription_id__first_name__icontains=search_value, follower_id__id=user_id) |
            Q(subscription_id__last_name__icontains=search_value, follower_id__id=user_id)
        ).select_related("subscription_id")
    
    return list(query)


@database_sync_to_async
def get_users_search(search_value: str, user_id: int) -> list:
    """Get user by search"""

    query = User.objects.exclude(id=user_id).filter(
            Q(username__icontains=search_value) | 
            Q(first_name__icontains=search_value) |
            Q(last_name__icontains=search_value)
        )[:10]
    
    return list(query)