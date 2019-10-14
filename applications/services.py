from conf.client import get, post, put, delete
from conf.constants import CASE_NOTES_URL, APPLICATIONS_URL, CASES_URL, ECJU_QUERIES_URL


def get_application(request, pk):
    data = get(request, APPLICATIONS_URL + pk + '/')
    return data.json(), data.status_code


def get_applications(request):
    data = get(request, APPLICATIONS_URL + '?submitted=true')
    return data.json()['applications']


def delete_application_preexisting_good(request, good_on_application_pk):
    response = delete(request, APPLICATIONS_URL + 'good-on-application/' + good_on_application_pk)
    return response.status_code


# Case related
def get_case_notes(request, pk):
    data = get(request, CASES_URL + pk + CASE_NOTES_URL)
    return data.json()


def post_application_case_notes(request, pk, json):
    data = post(request, CASES_URL + pk + CASE_NOTES_URL, json)
    return data.json(), data.status_code


def get_ecju_query(request, pk, query_pk):
    data = get(request, CASES_URL + pk + ECJU_QUERIES_URL + query_pk).json()['ecju_query']
    return data


def put_ecju_query(request, pk, query_pk, json):
    data = put(request, CASES_URL + pk + ECJU_QUERIES_URL + query_pk + '/', json)
    return data.json(), data.status_code


def get_application_ecju_queries(request, pk):
    data = get(request, CASES_URL + pk + ECJU_QUERIES_URL).json()['ecju_queries']

    open_queries = [x for x in data if not x['response']]
    closed_queries = [x for x in data if x['response']]

    return open_queries, closed_queries


def set_application_status(request, pk, status):
    json = {'status': status}
    data = put(request, APPLICATIONS_URL + pk + '/', json)
    return data.json(), data.status_code
