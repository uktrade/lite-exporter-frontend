from http import HTTPStatus


def validate_opening_question(_, json):
    if json.get("licence_type"):
        return json, HTTPStatus.OK

    return (
        {"errors": {"licence_type": ["Select the type of licence or clearance you need"]}},
        HTTPStatus.BAD_REQUEST,
    )


def validate_open_general_licences(_, json):
    if not json.get("control_list_entry"):
        return (
            {"errors": {"control_list_entry": ["Select a control list entry"]}},
            HTTPStatus.BAD_REQUEST,
        )

    if not json.get("country"):
        return (
            {"errors": {"country": ["Select a country"]}},
            HTTPStatus.BAD_REQUEST,
        )

    if not json.get("open_general_licence"):
        return (
            {"errors": {"open_general_licence": ["Select the type of licence you want to apply for"]}},
            HTTPStatus.BAD_REQUEST,
        )

    return json, HTTPStatus.OK
