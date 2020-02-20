from http import HTTPStatus
from urllib.parse import urlencode

from django.http import StreamingHttpResponse

from core.helpers import convert_parameters_to_query_params
from lite_content.lite_exporter_frontend.generic import Document
from lite_forms.components import Option, TextArea

from conf.client import get, post, put, delete
from conf.constants import (
    UNITS_URL,
    APPLICATIONS_URL,
    STATIC_COUNTRIES_URL,
    EXTERNAL_LOCATIONS_URL,
    NOTIFICATIONS_URL,
    ORGANISATIONS_URL,
    CASES_URL,
    CONTROL_LIST_ENTRIES_URL,
    NEWLINE,
    PV_GRADINGS_URL,
    ITEM_TYPES_URL,
)
from lite_forms.generators import error_page


def get_units(request):
    data = get(request, UNITS_URL).json().get("units")
    return [Option(key, value) for key, value in data.items()]


def get_item_types(request):
    data = get(request, ITEM_TYPES_URL).json().get("item_types")
    options = []
    for k, v in data.items():
        if k == "other":
            options.append(
                Option(
                    key=k,
                    value=v,
                    components=[
                        TextArea(
                            title="", description="", name="other_item_type", extras={"max_length": 100}, classes=[]
                        ),
                    ],
                )
            )
        else:
            options.append(Option(key=k, value=v))
    return options


def get_countries(request, convert_to_options=False):
    data = get(request, STATIC_COUNTRIES_URL).json()["countries"]

    if convert_to_options:
        return [Option(x["id"], x["name"]) for x in data]

    return data


def get_sites_on_draft(request, pk):
    data = get(request, APPLICATIONS_URL + pk + "/sites/")
    return data.json(), data.status_code


def post_sites_on_draft(request, pk, json):
    data = post(request, APPLICATIONS_URL + pk + "/sites/", json)
    return data.json(), data.status_code


def get_external_locations(request, pk, formatted=False):
    data = get(request, ORGANISATIONS_URL + str(pk) + EXTERNAL_LOCATIONS_URL)

    if formatted:
        external_locations_options = []

        for external_location in data.json().get("external_locations"):
            external_location_id = external_location.get("id")
            external_location_name = external_location.get("name")
            external_location_address = (
                external_location.get("address") + NEWLINE + external_location.get("country").get("name")
            )

            external_locations_options.append(
                Option(external_location_id, external_location_name, description=external_location_address)
            )

        return external_locations_options

    return data.json(), data.status_code


def get_external_locations_on_draft(request, pk):
    data = get(request, APPLICATIONS_URL + pk + "/external_locations/")
    return data.json(), data.status_code


def delete_external_locations_from_draft(request, pk, ext_loc_pk):
    data = delete(request, APPLICATIONS_URL + pk + "/external_locations/" + ext_loc_pk + "/")
    return data.status_code


def post_external_locations_on_draft(request, pk, json):
    data = post(request, APPLICATIONS_URL + pk + "/external_locations/", json)
    return data.json(), data.status_code


def post_external_locations(request, pk, json):
    data = post(request, ORGANISATIONS_URL + pk + EXTERNAL_LOCATIONS_URL, json)
    return data.json(), data.status_code


def get_notifications(request):
    data = get(request, NOTIFICATIONS_URL)
    return data.json(), data.status_code


# Organisation
def get_organisations(request, page: int = 1, search_term=None, org_type=None):
    """
    Returns a list of organisations
    :param request: Standard HttpRequest object
    :param page: Returns n page of page results
    :param search_term: Filter by name
    :param org_type: Filter by org type - 'hmrc', 'commercial', 'individual', or an array of it
    """
    data = get(request, ORGANISATIONS_URL + convert_parameters_to_query_params(locals()))
    return data.json()


def get_organisation(request, pk):
    """
    Returns an organisation
    """
    data = get(request, ORGANISATIONS_URL + str(pk))
    return data.json()


def get_organisation_users(request, pk, params):
    data = get(request, ORGANISATIONS_URL + pk + "/users/?" + urlencode(params))
    return data.json(), data.status_code


def get_organisation_user(request, pk, user_pk):
    data = get(request, ORGANISATIONS_URL + pk + "/users/" + user_pk)
    return data.json()["user"]


def put_organisation_user(request, user_pk, json):
    organisation_id = str(request.user.organisation)
    data = put(request, ORGANISATIONS_URL + organisation_id + "/users/" + str(user_pk) + "/", json)
    return data.json(), data.status_code


# Cases
def get_case(request, pk):
    data = get(request, CASES_URL + pk)
    return data.json().get("case") if data.status_code == HTTPStatus.OK else None


# Control List Entries
def get_control_list_entries(request, convert_to_options=False):
    if convert_to_options:
        data = get(request, CONTROL_LIST_ENTRIES_URL + "?flatten=True")

        converted_units = []

        for control_list_entry in data.json().get("control_list_entries"):
            converted_units.append(
                Option(
                    key=control_list_entry["rating"],
                    value=control_list_entry["rating"],
                    description=control_list_entry["text"],
                )
            )

        return converted_units

    data = get(request, CONTROL_LIST_ENTRIES_URL)
    return data.json().get("control_list_entries")


# PV gradings
def get_pv_gradings(request, convert_to_options=False):
    if convert_to_options:
        data = get(request, PV_GRADINGS_URL)

        converted_units = []
        for pvg in data.json().get("pv_gradings"):
            for key in pvg:
                converted_units.append(Option(key=key, value=pvg[key],))
        return converted_units

    data = get(request, PV_GRADINGS_URL)
    return data.json().get("pv-gradings")


def get_control_list_entry(request, rating):
    data = get(request, CONTROL_LIST_ENTRIES_URL + rating)
    return data.json().get("control_list_entry")


def get_document_download_stream(request, url):
    response = get(request, url)
    if response.status_code == HTTPStatus.OK:
        return StreamingHttpResponse(response, content_type=response.headers._store["content-type"][1])
    elif response.status_code == HTTPStatus.UNAUTHORIZED:
        error = Document.ACCESS_DENIED
    else:
        error = Document.DOWNLOAD_ERROR
    return error_page(request, error)
