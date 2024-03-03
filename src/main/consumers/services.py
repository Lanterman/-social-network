def create_dict_of_user(user) -> dict:
    """Create a dictionary of a user"""

    return {
        "user_pk": user.id,
        "user_url": user.get_absolute_url(),
        "user_full_name": user.get_full_name().title(),
        "user_photo": user.photo.url if user.photo else None,
    }

