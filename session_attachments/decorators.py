# -*- coding: utf-8 -*-
from functools import wraps


def enforce_session(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        request.session.modified = True
        return view(request, *args, **kwargs)
    return wrapper
