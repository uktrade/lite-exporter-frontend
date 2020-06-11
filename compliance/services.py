from http import HTTPStatus

from django.http import HttpResponse

from conf.client import post, get
from conf.constants import MAX_OPEN_LICENCE_RETURNS_FILE_SIZE


def get_open_licence_returns(request):
    data = get(request, "/compliance/open-licence-returns/")
    return data.json()


def get_open_licence_return_download(request, pk):
    data = get(request, "/compliance/open-licence-returns/" + str(pk) + "/")
    open_licence_returns = data.json()
    response = HttpResponse("\n" + open_licence_returns["file"], content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="{open_licence_returns["year"]}OpenLicenceReturns.csv"'
    return response


def post_open_licence_return(request, json):
    if not json.get("year"):
        return {"errors": {"year": ["No year selected"]}}, HTTPStatus.BAD_REQUEST

    if len(request.FILES) == 0:
        return {"errors": {"file": ["No file"]}}, HTTPStatus.BAD_REQUEST
    if len(request.FILES) != 1:
        return {"errors": {"file": ["Multiple files"]}}, HTTPStatus.BAD_REQUEST
    if request.FILES["file"].size > MAX_OPEN_LICENCE_RETURNS_FILE_SIZE:
        return {"errors": {"file": ["File too large"]}}, HTTPStatus.BAD_REQUEST

    try:
        file = request.FILES.pop("file")[0]
        json["file"] = file.read().decode("utf-8")
    except Exception:  # noqa
        return {"errors": {"file": ["Failed to read file. Ensure you upload a CSV"]}}, HTTPStatus.BAD_REQUEST

    data = post(request, "/compliance/open-licence-returns/", json)
    return data.json(), data.status_code
