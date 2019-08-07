from urllib.parse import urlencode

from conf.client import get, post, put, delete
from conf.constants import GOODS_URL, DOCUMENTS_URL


def get_goods(request, params=None):
    if params:
        query_params = urlencode(params)
        data = get(request, GOODS_URL + '?' + query_params)
    else:
        data = get(request, GOODS_URL)

    return data.json(), data.status_code


def get_good(request, pk):
    data = get(request, GOODS_URL + pk)
    return data.json(), data.status_code


def post_goods(request, json):
    data = post(request, GOODS_URL, json)
    return data.json(), data.status_code


def update_good(request, pk, json):
    data = put(request, GOODS_URL + pk + "/", json)
    return data.json(), data.status_code


def delete_good(request, pk):
    data = delete(request, GOODS_URL + pk)
    return data.json(), data.status_code


# Documents
def get_good_document(request, pk, s3_key):
    data = get(request, GOODS_URL + pk + DOCUMENTS_URL + s3_key)
    return data.json(), data.status_code


def get_good_documents(request, pk):
    data = get(request, GOODS_URL + pk + DOCUMENTS_URL)
    return data.json(), data.status_code


def post_good_documents(request, pk, json):
    data = post(request, GOODS_URL + pk + DOCUMENTS_URL, json)
    return data.json(), data.status_code


def delete_good_document(request, pk, s3_key):
    data = delete(request, GOODS_URL + pk + DOCUMENTS_URL + s3_key)
    return data.json(), data.status_code
