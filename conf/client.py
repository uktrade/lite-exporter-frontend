import json

import requests
from django.contrib.auth.models import AnonymousUser
from mohawk import Sender

from conf.settings import env


def get(request, appended_address):
    url = _build_absolute_uri(appended_address.replace(" ", "%20"))

    sender = _get_hawk_sender(url, "GET", "application/json", None)

    response = requests.get(url, headers=_get_headers(request, sender))

    _verify_api_response(response, sender)

    return response


def post(request, appended_address, request_data):
    url = _build_absolute_uri(appended_address)

    sender = _get_hawk_sender(url, "POST", "application/json", json.dumps(request_data))

    response = requests.post(url, json=request_data, headers=_get_headers(request, sender))

    _verify_api_response(response, sender)

    return response


def put(request, appended_address, request_data):
    url = _build_absolute_uri(appended_address)

    sender = _get_hawk_sender(url, "PUT", "application/json", json.dumps(request_data))

    response = requests.put(url, json=request_data, headers=_get_headers(request, sender))

    _verify_api_response(response, sender)

    return response


def patch(request, appended_address, request_data):
    url = _build_absolute_uri(appended_address)

    sender = _get_hawk_sender(url, "PATCH", "application/json", json.dumps(request_data))

    response = requests.patch(
        url=env("LITE_API_URL") + appended_address, json=request_data, headers=_get_headers(request, sender),
    )

    _verify_api_response(response, sender)

    return response


def delete(request, appended_address):
    url = _build_absolute_uri(appended_address)

    sender = _get_hawk_sender(url, "DELETE", "text/plain", None)

    response = requests.delete(url=env("LITE_API_URL") + appended_address, headers=_get_headers(request, sender))

    _verify_api_response(response, sender)

    return response


def _build_absolute_uri(appended_address):
    url = env("LITE_API_URL") + appended_address

    if not url.endswith("/") and "?" not in url:
        url = url + "/"

    return url


def _get_headers(request, sender):
    headers = {
        "X-Correlation-Id": str(request.correlation),
        "Authorization": sender.request_header,
        "content-type": sender.req_resource.content_type,
    }

    if not isinstance(request.user, AnonymousUser):
        headers["EXPORTER-USER-TOKEN"] = str(request.user.user_token)
        headers["ORGANISATION-ID"] = str(request.user.organisation)

    return headers


def _get_hawk_sender(url, method, content_type, content):
    return Sender(
        {"id": "exporter-frontend", "key": env("LITE_EXPORTER_HAWK_KEY"), "algorithm": "sha256"},
        url,
        method,
        content_type=content_type,
        content=content,
    )


def _verify_api_response(response, sender):
    sender.accept_response(
        response.headers["server-authorization"],
        content=response.content,
        content_type=response.headers["Content-Type"],
    )
