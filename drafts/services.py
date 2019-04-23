from conf.client import get, post, put, delete

DRAFTS_URL = '/drafts/'


def get_drafts(request):
    data = get(request, DRAFTS_URL)
    return data.json(), data.status_code


def get_draft(request, pk):
    data = get(request, DRAFTS_URL + pk)
    return data.json(), data.status_code


def post_drafts(request, json):
    data = post(request, DRAFTS_URL, json)
    return data.json(), data.status_code


def put_draft(request, pk, json):
    data = put(request, DRAFTS_URL + pk, json)
    return data.json(), data.status_code


def delete_draft(request, pk):
    data = delete(request, DRAFTS_URL + pk)
    return data.json(), data.status_code
