from http import HTTPStatus

from applications.services import set_application_status, delete_application
from lite_content.lite_exporter_frontend import strings


def validate_withdraw_application(request, pk, json):
    if json.get("choice"):
        if json.get("choice") == "yes":
            return set_application_status(request, pk, "withdrawn")
        return json, HTTPStatus.OK

    return {"errors": {"choice": [strings.APPLICATION_WITHDRAW_ERROR]}}, HTTPStatus.BAD_REQUEST


def validate_delete_draft(request, pk, json):
    if json.get("choice"):
        if json.get("choice") == "yes":
            return delete_application(request, pk)
        return json, HTTPStatus.OK

    return {"errors": {"choice": [strings.applications.DeleteApplicationPage.DELETE_ERROR]}}, HTTPStatus.BAD_REQUEST


def validate_external_location_choice(_request, _pk, json):
    if json.get("choice"):
        return json, HTTPStatus.OK

    return {"errors": {"choice": ["Select a choice"]}}, HTTPStatus.BAD_REQUEST
