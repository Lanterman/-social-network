def create_user(strategy, details, backend, user=None, *args, **kwargs):
    if user:
        return {"is_new": False}

    fields = {
        name: kwargs.get(name, details.get(name))
        for name in backend.setting("USER_FIELDS", ["username", "email"])
    }

    if not fields:
        return
    
    fields["slug"] = fields["username"]
    user1 = strategy.create_user(**fields)
    return {"is_new": True, "user": user1}

