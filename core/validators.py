from http import HTTPStatus


def validate_register_organisation_triage(_, json):
    errors = {}

    # TODO strings!

    if not json.get("type"):
        errors["type"] = ["Select the type of organisation you're registering for"]

    if not json.get("location"):
        errors["location"] = ["Select the type of organisation you're registering for"]

    if errors:
        return {"errors": errors}, HTTPStatus.BAD_REQUEST

    return json, HTTPStatus.OK
