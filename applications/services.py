from conf.client import get, post
from conf.constants import CASE_NOTES_URL, APPLICATIONS_URL, CASES_URL, ECJU_QUERIES_URL


def get_application(request, pk):
    data = get(request, APPLICATIONS_URL + pk)
    return data.json(), data.status_code


def get_applications(request):
    data = get(request, APPLICATIONS_URL)
    return data.json(), data.status_code


# Case related
def get_application_case_notes(request, pk):
    data = get(request, CASES_URL + pk + CASE_NOTES_URL)
    return data.json(), data.status_code


def post_application_case_notes(request, pk, json):
    data = post(request, CASES_URL + pk + CASE_NOTES_URL, json)
    return data.json(), data.status_code


def get_application_ecju_queries(request, pk):
    data = get(request, CASES_URL + pk + ECJU_QUERIES_URL)
    return data.json(), data.status_code
