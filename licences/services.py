from conf.client import get
from conf.constants import LICENCES_URL


def get_licences(request, params):
    data = get(request, LICENCES_URL + "?" + params)
    return data.json()
