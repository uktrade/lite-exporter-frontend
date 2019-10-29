from conf.client import get
from conf.constants import ORGANISATIONS_URL
from core.helpers import convert_parameters_to_query_params


def get_organisations(request, page: int = 0, name=None, org_type=None):
    """
    Returns a list of organisations
    :param request: Standard HttpRequest object
    :param page: Returns n page of page results
    :param name: Filter by name
    :param org_type: Filter by org type - 'hmrc', 'commercial', 'individual'
    """
    data = get(request, ORGANISATIONS_URL + convert_parameters_to_query_params(locals()))
    return data.json()


def get_organisation(request, pk):
    """
    Returns an organisation
    """
    data = get(request, ORGANISATIONS_URL + pk)
    return data.json()
