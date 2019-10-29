from conf.client import get
from conf.constants import ORGANISATIONS_URL
from core.helpers import convert_parameters_to_query_params


def get_organisations(request,
                      page=0,
                      name=None,
                      org_type=None):
    data = get(request, ORGANISATIONS_URL + convert_parameters_to_query_params(locals()))
    return data.json(), data.status_code
