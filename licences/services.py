from conf.client import get
from conf.constants import LICENCES_URL
from core.helpers import convert_dict_to_query_params


def get_licences(request, page, type=None, reference=None, clc=None, country=None, end_user=None, active_only=None):
    data = get(request, LICENCES_URL + "?" + convert_dict_to_query_params(locals()))
    return data.json()
