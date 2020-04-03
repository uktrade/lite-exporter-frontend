from conf.client import get
from conf.constants import LICENCES_URL
from core.helpers import convert_dict_to_query_params


def get_licences(request, page, type=None, reference=None, clc=None, country=None, end_user=None, active_only=None):
    params = convert_dict_to_query_params({
        "page": page,
        "type": type,
        "reference": reference,
        "clc": clc,
        "country": country,
        "end_user": end_user,
        "active_only": active_only,
    })
    data = get(request, LICENCES_URL + "?" + params)
    return data.json()
