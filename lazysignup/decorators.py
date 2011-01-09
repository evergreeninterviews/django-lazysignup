from functools import wraps

from lazysignup.utils import start_lazy_user_session, username_from_session

def allow_lazy_user(func):
    def wrapped(request, *args, **kwargs):
        start_lazy_user_session(request)
        return func(request, *args, **kwargs)
    return wraps(func)(wrapped)
