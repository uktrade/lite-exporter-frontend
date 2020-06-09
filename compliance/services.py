from http import HTTPStatus

from conf.client import post
from conf.constants import MAX_ANNUAL_RETURNS_FILE_SIZE


def post_annual_return(request, json):
    if len(request.FILES) == 0:
        return {"errors": {"file": ["No file"]}}, HTTPStatus.BAD_REQUEST
    if len(request.FILES) != 1:
        return {"errors": {"file": ["Multiple files"]}}, HTTPStatus.BAD_REQUEST
    if request.FILES["file"].size > MAX_ANNUAL_RETURNS_FILE_SIZE:
        return {"errors": {"file": ["File too large"]}}, HTTPStatus.BAD_REQUEST

    try:
        file = request.FILES.pop("file")[0]
        json["file"] = file.read().decode("utf-8")
    except Exception:  # noqa
        return {"errors": {"file": ["Failed to read file. Ensure you upload a CSV"]}}, HTTPStatus.BAD_REQUEST

    data = post(request, "/compliance/open-licence-returns/", json)
    return data.json(), data.status_code
