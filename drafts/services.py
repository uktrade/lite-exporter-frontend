import logging

from conf.client import get, post, put, delete
from conf.constants import APPLICATIONS_URL, DRAFTS_URL, END_USER_DOCUMENT_URL, ULTIMATE_END_USER_URL, DOCUMENT_URL


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
    data = put(request, DRAFTS_URL + pk + '/', json)
    return data.json(), data.status_code


def delete_draft(request, pk):
    data = delete(request, DRAFTS_URL + pk)
    return data.json(), data.status_code


def submit_draft(request, pk):
    data = post(request, APPLICATIONS_URL, {'id': pk})
    return data.json(), data.status_code


# Goods
def get_draft_goods(request, pk):
    data = get(request, DRAFTS_URL + pk + '/goods/')
    return data.json(), data.status_code


def get_draft_goods_type(request, pk):
    data = get(request, DRAFTS_URL + pk + '/goodstype/')
    return data.json(), data.status_code


def get_draft_good(request, pk, good_pk):
    data = get(request, DRAFTS_URL + pk + '/goods/' + good_pk + '/')
    return data.json(), data.status_code


def post_draft_preexisting_goods(request, pk, json):
    data = post(request, DRAFTS_URL + pk + '/goods/', json)
    return data.json(), data.status_code


def post_end_user(request, pk, json):
    data = post(request, DRAFTS_URL + pk + '/end-user/', json)
    return data.json(), data.status_code


# Ultimate End Users
def get_ultimate_end_users(request, pk):
    data = get(request, DRAFTS_URL + pk + '/ultimate-end-users/')
    return data.json(), data.status_code


def post_ultimate_end_user(request, pk, json):
    data = post(request, DRAFTS_URL + pk + '/ultimate-end-users/', json)
    return data.json(), data.status_code


def delete_ultimate_end_user(request, pk, ueu_pk):
    data = delete(request, DRAFTS_URL + pk + '/ultimate-end-users/' + ueu_pk)
    return data.json(), data.status_code


# Countries
def get_draft_countries(request, pk):
    data = get(request, DRAFTS_URL + pk + '/countries/')
    return data.json(), data.status_code


def post_draft_countries(request, pk, json):
    data = post(request, DRAFTS_URL + pk + '/countries/', json)
    return data.json(), data.status_code


# End user Documents
def get_end_user_document(request, pk):
    data = get(request, DRAFTS_URL + pk + END_USER_DOCUMENT_URL)
    return data.json(), data.status_code


def post_end_user_document(request, pk, json):
    data = post(request, DRAFTS_URL + pk + END_USER_DOCUMENT_URL, json)
    return data.json(), data.status_code


def delete_end_user_document(request, pk):
    data = delete(request, DRAFTS_URL + pk + END_USER_DOCUMENT_URL)
    return data.status_code


# Ultimate end user Documents
def get_ultimate_end_user_document(request, pk, ueu_pk):
    data = get(request, DRAFTS_URL + pk + ULTIMATE_END_USER_URL + ueu_pk + DOCUMENT_URL)
    return data.json(), data.status_code


def post_ultimate_end_user_document(request, pk, ueu_pk, json):
    data = post(request, DRAFTS_URL + pk + ULTIMATE_END_USER_URL + ueu_pk + DOCUMENT_URL, json)
    return data.json(), data.status_code


def delete_ultimate_end_user_document(request, pk, ueu_pk):
    data = delete(request, DRAFTS_URL + pk + ULTIMATE_END_USER_URL + ueu_pk + DOCUMENT_URL)
    return data.status_code


# Third parties
def get_third_parties(request, pk):
    data = get(request, DRAFTS_URL + pk + '/third-parties/')
    return data.json(), data.status_code


def post_third_party(request, pk, json):
    data = post(request, DRAFTS_URL + pk + '/third-parties/', json)
    return data.json(), data.status_code


def delete_third_party(request, pk, tp_pk):
    data = delete(request, DRAFTS_URL + pk + '/third-parties/' + tp_pk)
    return data.status_code


# Consignee
def post_consignee(request, pk, json):
    data = post(request, DRAFTS_URL + pk + '/consignee/', json)
    return data.json(), data.status_code
