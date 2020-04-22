import datetime
from html import escape
from typing import List

from django.template.defaultfilters import safe
from django.templatetags.tz import do_timezone
from django.utils.safestring import mark_safe

from conf import decorators
from conf.constants import ISO8601_FMT
from core.builtins.custom_tags import default_na
from organisation.roles.services import get_user_permissions


class Section:
    def __init__(self, title, tiles):
        self.title = title
        self.tiles = tiles


class Tile:
    def __init__(self, title, description, url):
        self.title = title
        self.description = description
        self.url = url


def str_to_bool(v, invert_none=False):
    if v is None:
        return invert_none
    if isinstance(v, bool):
        return v
    return v.lower() in ("yes", "true", "t", "1")


def str_date_only(value):
    return_value = do_timezone(datetime.datetime.strptime(value, ISO8601_FMT), "Europe/London")
    return return_value.strftime("%d %B %Y")


def generate_notification_string(notifications, case_types):
    notification_count = notifications["notifications"]
    notification_count_sum = sum([count for case_type, count in notification_count.items() if case_type in case_types])
    return generate_notification_total_string(notification_count_sum)


def generate_notification_total_string(notification_count):
    if not notification_count:
        return ""
    elif notification_count == 1:
        return f"You have {notification_count} new notification"
    else:
        return f"You have {notification_count} new notifications"


def convert_value_to_query_param(key: str, value):
    """
    Convert key/value pairs to a string suitable for query parameters
    eg {'type': 'organisation'} becomes type=organisation
    eg {'type': ['organisation', 'organisation']} becomes type=organisation&type=organisation
    """
    if value is None:
        return ""

    if isinstance(value, list):
        return_value = ""
        for item in value:
            if not return_value:
                return_value = return_value + key + "=" + item
            else:
                return_value = return_value + "&" + key + "=" + item
        return return_value

    return key + "=" + str(value)


def convert_dict_to_query_params(dictionary: dict):
    return "&".join(([convert_value_to_query_param(key, value) for (key, value) in dictionary.items()]))


def convert_parameters_to_query_params(dictionary: dict):
    """
    Given a dictionary of parameters, convert to a query param string
    Removes request object and deletes empty keys
    """
    if "request" in dictionary:
        del dictionary["request"]

    return "?" + convert_dict_to_query_params({key: value for key, value in dictionary.items() if value is not None})


def convert_to_link(address, name=None, classes="", include_br=False):
    """
    Returns a correctly formatted, safe link to an address
    Returns default_na if no address is provided
    """
    if not address:
        return default_na(None)

    if not name:
        name = address

    address = escape(address)
    name = escape(name)

    br = "<br>" if include_br else ""

    return safe(f'<a href="{address}" class="govuk-link govuk-link--no-visited-state {classes}">{name}</a>{br}')


def remove_prefix(json, prefix):
    post_data = {}
    for k in json:
        if k.startswith(prefix):
            field = k[len(prefix) :]
            post_data[field] = json[k]
    return post_data


def println(content=None, no=1):
    print("\n" * no)
    if content:
        print(content)
        print("\n" * no)


def has_permission(request, permission):
    """
    Returns true if the user has a given permission, else false
    """
    user_permissions = get_user_permissions(request)
    return permission in user_permissions, user_permissions


def decorate_patterns_with_permission(patterns, permission, ignore: List[str] = None):
    def _wrap_with_permission(_permission, view_func=None):
        actual_decorator = decorators.has_permission(_permission)

        if view_func:
            return actual_decorator(view_func)
        return actual_decorator

    if ignore is None:
        ignore = []

    decorated_patterns = []
    for pattern in patterns:
        callback = pattern.callback
        if pattern.name in ignore:
            continue
        pattern.callback = _wrap_with_permission(permission, callback)
        pattern._callback = _wrap_with_permission(permission, callback)
        decorated_patterns.append(pattern)
    return decorated_patterns


def add_validate_only_to_data(data):
    data = data.copy()
    data["validate_only"] = True

    return data


def convert_control_list_entries(control_list_entries):
    return default_na(
        mark_safe(  # nosec
            ", ".join(
                [
                    "<span data-definition-title='"
                    + clc["rating"]
                    + "' data-definition-text='"
                    + clc["text"]
                    + "'>"
                    + clc["rating"]
                    + "</span>"
                    for clc in control_list_entries
                ]
            )
        )
    )
