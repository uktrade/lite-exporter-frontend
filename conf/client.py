import requests
from mohawk import Sender

from conf.settings import env


def get(request, appended_address):
    url = env("LITE_API_URL") + appended_address

    if not url.endswith("/") and "?" not in url:
        url = url + "/"

    sender = _get_hawk_sender(url, "GET", "text/plain", {})

    if request:
        response = requests.get(url, headers=_get_headers(request, sender),)

        _verify_api_response(response, sender)

        return response

    return requests.get(url)


def post(request, appended_address, json):
    if not appended_address.endswith("/"):
        appended_address = appended_address + "/"

    url = env("LITE_API_URL") + appended_address

    sender = _get_hawk_sender(url, "POST", "application/json", json)

    return requests.post(url, json=json, headers=_get_headers(request, sender),)


def put(request, appended_address: str, json):
    if not appended_address.endswith("/"):
        appended_address = appended_address + "/"

    url = env("LITE_API_URL") + appended_address

    sender = _get_hawk_sender(url, "PUT", "application/json", json)

    return requests.put(url, json=json, headers=_get_headers(request, sender),)


def patch(request, appended_address: str, json):
    if not appended_address.endswith("/"):
        appended_address = appended_address + "/"

    url = env("LITE_API_URL") + appended_address

    sender = _get_hawk_sender(url, "PATCH", "application/json", json)

    return requests.patch(url=env("LITE_API_URL") + appended_address, json=json, headers=_get_headers(request, sender),)


def delete(request, appended_address):
    if not appended_address.endswith("/"):
        appended_address = appended_address + "/"

    url = env("LITE_API_URL") + appended_address

    sender = _get_hawk_sender(url, "DELETE", "text/plain", {})

    return requests.delete(url=env("LITE_API_URL") + appended_address, headers=_get_headers(request, sender),)


def _get_headers(request, sender: Sender):
    return {
        "EXPORTER-USER-TOKEN": str(request.user.user_token),
        "X-Correlation-Id": str(request.correlation),
        "ORGANISATION-ID": str(request.user.organisation),
        "Authorization": sender.request_header,
    }


def _get_hawk_sender(url: str, method: str, content_type: str, content):
    return Sender(
        {"id": "exporter-frontend", "key": env("HAWK_KEY"), "algorithm": "sha256"},
        url,
        method,
        content=content,
        content_type=content_type,
    )


def _verify_api_response(response, sender: Sender):
    # TODO: Consider getting rid of this if stmt, assuming we expect all API responses to have this header
    if "server-authorization" in response.headers:
        sender.accept_response(
            response.headers["server-authorization"],
            content=response.content,
            content_type=response.headers["Content-Type"],
        )
