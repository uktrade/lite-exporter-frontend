from conf.client import get, post, put
from conf.constants import SITES_URL, ORGANISATIONS_URL, ROLES_URL, EXPORTER_USERS_PERMISSIONS_URL, SUPER_USER_ROLE_ID
from core.helpers import println
from lite_forms.components import Option
from users.services import get_user


def get_site(request, organisation_id, pk):
    data = get(request, ORGANISATIONS_URL + organisation_id + SITES_URL + pk)
    return data.json(), data.status_code


def put_site(request, organisation_id, pk, json):
    data = put(request, ORGANISATIONS_URL + organisation_id + SITES_URL + pk + '/', json=json)
    return data.json(), data.status_code


def post_sites(request, organisation_id, json):
    data = post(request, ORGANISATIONS_URL + organisation_id + SITES_URL, json)
    return data.json(), data.status_code


def get_roles(request, organisation_id, convert_to_options=False):
    data = get(request, ORGANISATIONS_URL + str(organisation_id) + ROLES_URL)
    data = data.json()['results']

    if convert_to_options:
        converted = []

        for item in data.json().get("roles"):
            converted.append(Option(key=item["id"], value=item["name"]))

        return converted

    return data


def get_role(request, pk):
    organisation_id = str(request.user.organisation)
    data = get(request, ORGANISATIONS_URL + str(organisation_id) + ROLES_URL + str(pk))
    return data.json()['role']


def post_role(request, json):
    organisation_id = str(request.user.organisation)
    data = post(request, ORGANISATIONS_URL + str(organisation_id) + ROLES_URL, json)
    return data.json(), data.status_code


def put_role(request, pk, json):
    organisation_id = request.user.organisation
    data = put(request, ORGANISATIONS_URL + str(organisation_id) + ROLES_URL + str(pk) + "/", json)
    return data.json(), data.status_code


def get_permissions(request, convert_to_options=False):
    data = get(request, EXPORTER_USERS_PERMISSIONS_URL)

    if convert_to_options:
        converted = []

        for item in data.json().get("permissions"):
            converted.append(Option(key=item["id"], value=item["name"]))

        return converted

    return data.json()["permissions"]


def get_user_permissions(request):
    user, _ = get_user(request)
    return user["user"]["role"]["permissions"]


def is_super_user(user):
    return user["user"]["role"]["id"] == SUPER_USER_ROLE_ID
