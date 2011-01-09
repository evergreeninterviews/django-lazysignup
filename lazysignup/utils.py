import hashlib

from django.conf import settings
from django.contrib.auth import SESSION_KEY
from django.contrib.auth import authenticate
from django.contrib.auth import get_user
from django.contrib.auth import login
from django.contrib.auth.models import User


USER_AGENT_BLACKLIST = []

def start_lazy_user_session(request):
    assert hasattr(request, 'session'), "You need to have the session app installed"

    if getattr(settings, 'LAZYSIGNUP_ENABLE', True):
        # If the user agent is one we ignore, bail early
        ignore = False
        request_user_agent = request.META.get('HTTP_USER_AGENT', '')
        for user_agent in USER_AGENT_BLACKLIST:
            if user_agent.search(request_user_agent):
                ignore = True
                break

        # If there's already a key in the session for a valid user, then we don't
        # need to do anything. If the user isn't valid, then get_user will return
        # an anonymous user
        if get_user(request).is_anonymous() and not ignore:
            # If not, then we have to create a user, and log them in. Set the user id
            # in the session here to prevent the login call cycling the session key.
            username = username_from_session(request.session.session_key)

            User.objects.create_user(username, '')
            request.user = None
            user = authenticate(username=username)
            assert user, "Lazy user creation and authentication failed. Have you got lazysignup.backends.LazySignupBackend in AUTHENTICATION_BACKENDS?"
            request.session[SESSION_KEY] = user.id
            login(request, user)

def username_from_session(session_key, username_length=None):
    if not username_length:
        username_length = User._meta.get_field('username').max_length
    return hashlib.sha1(session_key).hexdigest()[:username_length]
