from conf.client import get
from conf.constants import LICENCES_URL
from core.helpers import convert_dict_to_query_params


def get_licences(
    request, page=None, licence_type=None, reference=None, clc=None, country=None, end_user=None, active_only=None
):
    if not page:
        page = 1
    data = get(request, LICENCES_URL + "?" + convert_dict_to_query_params(locals()))
    return data.json()
