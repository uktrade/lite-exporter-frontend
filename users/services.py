from conf.client import get, post, put
from conf.constants import USERS_URL, SUPER_USER_ROLE_ID


def get_user(request, pk=None):
    if pk:
        data = get(request, USERS_URL + pk)
    else:
        data = get(request, USERS_URL + "me/")
    return data.json(), data.status_code


def get_users(request):
    data = get(request, USERS_URL)
    return data.json(), data.status_code


def post_users(request, json):
    data = post(request, USERS_URL, json)
    return data.json(), data.status_code


def update_user(request, pk, json):
    data = put(request, USERS_URL + pk + "/", json)
    return data.json(), data.status_code


def is_super_user(user):
    if "user" in user:
        return user["user"]["role"]["id"] == SUPER_USER_ROLE_ID
    else:
        return user["role"]["id"] == SUPER_USER_ROLE_ID
