import datetime

from pytest import fixture

from helpers.utils import Timer, get_lite_client


@fixture(scope='module')
def add_an_application(driver, request, api_url, exporter_url, context, exporter_sso_login_info):
    timer = Timer()
    lite_client = get_lite_client(context, api_url, exporter_login=exporter_sso_login_info)

    app_time_id = datetime.datetime.now().strftime(' %d%H%M%S')
    context.app_time_id = app_time_id
    app_name = 'Test Application' + app_time_id

    lite_client.add_draft(
        draft={
            "name": app_name,
            "licence_type": "standard_licence",
            "export_type": "permanent",
            "have_you_been_informed": "yes",
            "reference_number_on_information_form": "1234"},
        good={
            "good_id": "",
            "quantity": 1234,
            "unit": "MTR",
            "value": 1},
        enduser={
            "name": "Mr Smith",
            "address": "London",
            "country": "UA",
            "sub_type": "government",
            "website": "https://www.smith.com"
        },
        ultimate_end_user={
            "name": "Individual",
            "address": "Bullring, Birmingham SW1A 0AA",
            "country": "GB",
            "sub_type": "commercial",
            "website": "https://www.anothergov.uk"
        },
        consignee={
             'name': 'Government',
             'address': 'Westminster, London SW1A 0BB',
             'country': 'GB',
             'sub_type': 'government',
             'website': 'https://www.gov.uk'
        }
    )
    lite_client.submit_application()
    context.app_id = lite_client.context['application_id']
    context.app_name = app_name
    context.case_id = lite_client.context['case_id']
    lite_client.add_ecju_query(context.case_id)
    timer.print_time('apply_for_standard_application')
