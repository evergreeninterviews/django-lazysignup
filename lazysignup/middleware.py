from lazysignup.utils import start_lazy_user_session


class LazySignupMiddleware(object):
    """Allow lazy users by specifying kwargs in an urlpatterns.

    Example::

        urlpatterns = patterns('',
            url(r'^myapp/', include('myapp.urls'), kwargs=dict(
                allow_lazy_user=True,
            )),
        )
    """

    def process_view(self, request, view_func, view_args, view_kwargs):
        allow_lazy_user = view_kwargs.pop('allow_lazy_user', False)
        if allow_lazy_user:
            start_lazy_user_session(request)
