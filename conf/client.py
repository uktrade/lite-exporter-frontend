import json
import requests
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied
from mohawk import Sender
from mohawk.exc import HawkFail

from conf.settings import HAWK_AUTHENTICATION_ENABLED, env


def get(request, appended_address):
    url = _build_absolute_uri(appended_address.replace(" ", "%20"))

    if HAWK_AUTHENTICATION_ENABLED:
        sender = _get_hawk_sender(url, "GET", "application/json", "")

        response = requests.get(url=url, headers=_get_headers(request, sender))

        _verify_api_response(response, sender)
    else:
        response = requests.get(url=url, headers=_get_headers(request, content_type="application/json"))

    return response


def post(request, appended_address, request_data):
    url = _build_absolute_uri(appended_address)

    if HAWK_AUTHENTICATION_ENABLED:
        sender = _get_hawk_sender(url, "POST", "application/json", json.dumps(request_data))

        response = requests.post(url=url, headers=_get_headers(request, sender), json=request_data)

        _verify_api_response(response, sender)
    else:
        response = requests.post(
            url=url, headers=_get_headers(request, content_type="application/json"), json=request_data
        )

    return response


def put(request, appended_address, request_data):
    url = _build_absolute_uri(appended_address)

    if HAWK_AUTHENTICATION_ENABLED:
        sender = _get_hawk_sender(url, "PUT", "application/json", json.dumps(request_data))

        response = requests.put(url=url, headers=_get_headers(request, sender), json=request_data)

        _verify_api_response(response, sender)
    else:
        response = requests.put(
            url=url, headers=_get_headers(request, content_type="application/json"), json=request_data
        )

    return response


def patch(request, appended_address, request_data):
    url = _build_absolute_uri(appended_address)

    if HAWK_AUTHENTICATION_ENABLED:
        sender = _get_hawk_sender(url, "PATCH", "application/json", json.dumps(request_data))

        response = requests.patch(url=url, headers=_get_headers(request, sender), json=request_data)

        _verify_api_response(response, sender)
    else:
        response = requests.patch(
            url=url, headers=_get_headers(request, content_type="application/json"), json=request_data
        )

    return response


def delete(request, appended_address):
    url = _build_absolute_uri(appended_address)

    if HAWK_AUTHENTICATION_ENABLED:
        sender = _get_hawk_sender(url, "DELETE", "text/plain", "")

        response = requests.delete(url=url, headers=_get_headers(request, sender))

        _verify_api_response(response, sender)
    else:
        response = requests.delete(url=url, headers=_get_headers(request, content_type="text/plain"))

    return response


def _build_absolute_uri(appended_address):
    url = env("LITE_API_URL") + appended_address

    if not url.endswith("/") and "?" not in url:
        url = url + "/"

    return url


def _get_headers(request, sender=None, content_type=None):
    headers = {"X-Correlation-Id": str(request.correlation)}

    if sender:
        headers["content-type"] = sender.req_resource.content_type
        headers["hawk-authentication"] = sender.request_header

    if content_type:
        headers["content-type"] = content_type

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
    try:
        sender.accept_response(
            response.headers["server-authorization"],
            content=response.content,
            content_type=response.headers["Content-Type"],
        )
    except HawkFail:
        raise PermissionDenied(
            "We were unable to authenticate you - This could be due to your request MAC being incorrect"
        )
    except Exception:
        raise PermissionDenied(
            "We were unable to authenticate you - This could be due to a missing "
            "'server-authorization' header from our API."
        )
