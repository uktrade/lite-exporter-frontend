from django.utils.functional import wraps

from conf.exceptions import PermissionDeniedError
from core import helpers


def acceptable_statuses(statuses: [int], with_status: bool = False):
    """ Check if an application is in an editable state. """

    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            data = func(request, *args, **kwargs)

            if data[1] not in statuses:
                raise Exception(f"Status code: {data[1]} was not expected during ' {func.__name__}()'")

            if with_status:
                return data

            else:
                return data[0]

        return inner

    return decorator


def has_permission(permission):
    """
    Decorator for views that checks that the user has a given permission
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if helpers.has_permission(request, permission):
                return view_func(request, *args, **kwargs)

            raise PermissionDeniedError(
                f"You don't have the permission '{permission}' to view this, "
                "check urlpatterns or the function decorator if you want to change "
                "this functionality."
            )

        return _wrapped_view

    return decorator
