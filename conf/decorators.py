from functools import wraps


def acceptable_statuses(statuses: [int]):
    """ Check if an application is in an editable state. """

    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            data = func(request, *args, **kwargs)

            if data[1] not in statuses:
                raise Exception("Status code was not expected during '" + str(func.__name__) + "()'")

            return data

        return inner

    return decorator
