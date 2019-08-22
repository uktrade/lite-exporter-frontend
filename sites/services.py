from conf.client import get, post, put
from conf.constants import SITES_URL, ORGANISATIONS_URL
from libraries.forms.components import Option


def get_sites(request, organisation_id, formatted=False):
    data = get(request, ORGANISATIONS_URL + organisation_id + SITES_URL)

    if formatted:
        sites_options = []

        for site in data.json().get('sites'):
            site_id = site.get('id')
            site_name = site.get('name')
            address = site.get('address')
            site_address = '\n'.join(filter(None, [address.get('address_line_1'),
                                                   address.get('address_line_2'),
                                                   address.get('postcode'),
                                                   address.get('city')]))

            sites_options.append(
                Option(site_id, site_name, description=site_address)
            )

        return sites_options

    return data.json(), data.status_code


def get_site(request, organisation_id, pk):
    data = get(request, ORGANISATIONS_URL + organisation_id + SITES_URL + pk)
    return data.json(), data.status_code


def put_site(request, organisation_id, pk, json):
    data = put(request, ORGANISATIONS_URL + organisation_id + SITES_URL + pk + '/', json=json)
    return data.json(), data.status_code


def post_sites(request, organisation_id, json):
    data = post(request, ORGANISATIONS_URL + organisation_id + SITES_URL, json)
    return data.json(), data.status_code
