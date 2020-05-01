import requests
from mohawk import Sender
from mohawk.base import HawkEmptyValue

from conf.settings import env


def get(request, appended_address):
    url = env("LITE_API_URL") + appended_address

    if not url.endswith("/") and "?" not in url:
        url = url + "/"

    if request:
        return requests.get(url, headers=_get_headers(request, url, "GET", "text/plain", {}),)

    return requests.get(url)


def post(request, appended_address, json):
    url = env("LITE_API_URL") + appended_address

    return requests.post(url, json=json, headers=_get_headers(request, url, "POST", "application/json", json),)


def put(request, appended_address: str, json):
    if not appended_address.endswith("/"):
        appended_address = appended_address + "/"

    url = env("LITE_API_URL") + appended_address

    return requests.put(url, json=json, headers=_get_headers(request, url, "PUT", "application/json", json),)


def patch(request, appended_address: str, json):
    if not appended_address.endswith("/"):
        appended_address = appended_address + "/"

    url = env("LITE_API_URL") + appended_address

    return requests.patch(
        url=env("LITE_API_URL") + appended_address,
        json=json,
        headers=_get_headers(request, url, "PATCH", "application/json", json),
    )


def delete(request, appended_address):
    url = env("LITE_API_URL") + appended_address

    return requests.delete(
        url=env("LITE_API_URL") + appended_address,
        headers=_get_headers(request, url, "DELETE", "application/json", ""),
    )


def _get_headers(request, url: str, method: str, content_type: str, content: str):
    return {
        "EXPORTER-USER-TOKEN": str(request.user.user_token),
        "X-Correlation-Id": str(request.correlation),
        "ORGANISATION-ID": str(request.user.organisation),
        "Authorization": _get_authorisation_header(url, method, content_type, content),
    }


def _get_authorisation_header(url: str, method: str, content_type: str, content: str):
    sender = Sender(
        {"id": "exporter-frontend", "key": "a long, complicated secret", "algorithm": "sha256"},
        url,
        method,
        content=content,
        content_type=content_type,
    )

    return sender.request_header
