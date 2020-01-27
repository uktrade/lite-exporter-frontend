from http import HTTPStatus

from conf.client import get, post, put, delete
from conf.constants import (
    ACTIVITY_URL,
    APPLICATIONS_URL,
    END_USER_DOCUMENT_URL,
    ULTIMATE_END_USER_URL,
    DOCUMENT_URL,
    CONSIGNEE_URL,
    THIRD_PARTIES_URL,
    CONSIGNEE_DOCUMENT_URL,
    APPLICATION_SUBMIT_URL,
    ADDITIONAL_DOCUMENT_URL,
    CASES_URL,
    CASE_NOTES_URL,
    ECJU_QUERIES_URL,
    MANAGE_STATUS_URL,
    GOODSTYPE_URL,
    GOODSTYPES_URL,
    GOODSTYPE_COUNTRY_URL,
    STATUS_PROPERTIES_URL,
    GENERATED_DOCUMENTS_URL,
    EXISTING_PARTIES_URL,
)
from conf.settings import AWS_STORAGE_BUCKET_NAME, STREAMING_CHUNK_SIZE
from django.http import StreamingHttpResponse
from s3chunkuploader.file_handler import s3_client

from core.helpers import remove_prefix, convert_parameters_to_query_params


def get_applications(request, page: int = 1, submitted: bool = True):
    """
    Returns a list of applications
    :param request: Standard HttpRequest object
    :param page: Returns n page of page results
    :param submitted: Returns submitted applications if True, else returns draft applications if False
    """
    data = get(request, APPLICATIONS_URL + convert_parameters_to_query_params(locals()))
    return data.json()


def get_application(request, pk):
    data = get(request, APPLICATIONS_URL + str(pk))
    return data.json()


def post_applications(request, json):
    data = post(request, APPLICATIONS_URL, json)
    return data.json(), data.status_code


def put_application(request, pk, json):
    data = put(request, APPLICATIONS_URL + str(pk), json)
    return data.json(), data.status_code


def delete_application(request, pk):
    data = delete(request, APPLICATIONS_URL + str(pk))
    return data.json(), data.status_code


def submit_application(request, pk):
    data = put(request, APPLICATIONS_URL + str(pk) + APPLICATION_SUBMIT_URL, json={})
    return data.json(), data.status_code


# Goods
def get_application_goods(request, pk):
    data = get(request, APPLICATIONS_URL + pk + "/goods/")
    return data.json().get("goods") if data.status_code == HTTPStatus.OK else None


def validate_application_good(request, pk, json):
    post_data = get_data_from_post_good_on_app(json)
    post_data["validate_only"] = True
    return post(request, APPLICATIONS_URL + pk + "/goods/", post_data)


def get_application_goods_types(request, pk):
    data = get(request, APPLICATIONS_URL + pk + "/goodstypes/")
    return data.json().get("goods") if data.status_code == HTTPStatus.OK else None


def post_good_on_application(request, pk, json):
    post_data = get_data_from_post_good_on_app(json)
    if "good_id" not in post_data:
        post_data["good_id"] = json["good_id"]
    data = post(request, APPLICATIONS_URL + str(pk) + "/goods/", post_data)
    return data.json(), data.status_code


def get_data_from_post_good_on_app(json):
    if json.get("good_on_app_value") or json.get("good_on_app_value") == "":
        post_data = remove_prefix(json, "good_on_app_")
    else:
        post_data = json
    return post_data


# Countries
def get_application_countries(request, pk):
    data = get(request, APPLICATIONS_URL + pk + "/countries/")
    return data.json()["countries"]


def post_application_countries(request, pk, json):
    data = post(request, APPLICATIONS_URL + pk + "/countries/", json)
    return data.json(), data.status_code


# End User
def post_end_user(request, pk, json):
    data = post(request, APPLICATIONS_URL + str(pk) + "/end-user/", json)
    return data.json(), data.status_code


# End user Documents
def get_end_user_document(request, pk):
    data = get(request, APPLICATIONS_URL + pk + END_USER_DOCUMENT_URL)
    return data.json(), data.status_code


def post_end_user_document(request, pk, json):
    data = post(request, APPLICATIONS_URL + pk + END_USER_DOCUMENT_URL, json)
    return data.json(), data.status_code


def delete_end_user(request, pk):
    data = delete(request, APPLICATIONS_URL + pk + "/end-user/")
    return data.status_code


def delete_end_user_document(request, pk):
    data = delete(request, APPLICATIONS_URL + pk + END_USER_DOCUMENT_URL)
    return data.status_code


# Ultimate End Users
def get_ultimate_end_users(request, pk):
    data = get(request, APPLICATIONS_URL + pk + "/ultimate-end-users/")
    return data.json()["ultimate_end_users"]


def post_ultimate_end_user(request, pk, json):
    data = post(request, APPLICATIONS_URL + str(pk) + "/ultimate-end-users/", json)
    return data.json(), data.status_code


def delete_ultimate_end_user(request, pk, obj_pk):
    data = delete(request, APPLICATIONS_URL + pk + "/ultimate-end-users/" + obj_pk)
    return data.status_code


# Ultimate end user Documents
def get_ultimate_end_user_document(request, pk, obj_pk):
    data = get(request, APPLICATIONS_URL + pk + ULTIMATE_END_USER_URL + str(obj_pk) + DOCUMENT_URL)
    return data.json(), data.status_code


def post_ultimate_end_user_document(request, pk, obj_pk, json):
    data = post(request, APPLICATIONS_URL + pk + ULTIMATE_END_USER_URL + str(obj_pk) + DOCUMENT_URL, json)
    return data.json(), data.status_code


def delete_ultimate_end_user_document(request, pk, obj_pk):
    data = delete(request, APPLICATIONS_URL + pk + ULTIMATE_END_USER_URL + str(obj_pk) + DOCUMENT_URL)
    return data.status_code


# Third parties
def get_third_parties(request, pk):
    data = get(request, APPLICATIONS_URL + pk + THIRD_PARTIES_URL)
    return data.json()["third_parties"]


def post_third_party(request, pk, json):
    data = post(request, APPLICATIONS_URL + str(pk) + THIRD_PARTIES_URL, json)
    return data.json(), data.status_code


def delete_third_party(request, pk, obj_pk):
    data = delete(request, APPLICATIONS_URL + pk + THIRD_PARTIES_URL + obj_pk)
    return data.status_code


def validate_third_party(request, pk, json):
    json = json.copy()
    json["validate_only"] = True

    data = post(request, APPLICATIONS_URL + str(pk) + THIRD_PARTIES_URL, json)
    return data.json(), data.status_code


# Third party Documents
def get_third_party_document(request, pk, obj_pk):
    data = get(request, APPLICATIONS_URL + str(pk) + THIRD_PARTIES_URL + str(obj_pk) + DOCUMENT_URL)
    return data.json(), data.status_code


def post_third_party_document(request, pk, obj_pk, json):
    data = post(request, APPLICATIONS_URL + str(pk) + THIRD_PARTIES_URL + str(obj_pk) + DOCUMENT_URL, json)
    return data.json(), data.status_code


def delete_third_party_document(request, pk, obj_pk):
    data = delete(request, APPLICATIONS_URL + str(pk) + THIRD_PARTIES_URL + str(obj_pk) + DOCUMENT_URL)
    return data.status_code


# Consignee
def post_consignee(request, pk, json):
    data = post(request, APPLICATIONS_URL + str(pk) + CONSIGNEE_URL, json)
    return data.json(), data.status_code


def delete_consignee(request, pk):
    data = delete(request, APPLICATIONS_URL + pk + CONSIGNEE_URL)
    return data.status_code


# Existing Parties
def get_existing_parties(request, pk, name=None, address=None, country=None):
    params = {"name": name, "address": address, "country": country}
    params = convert_parameters_to_query_params(params)
    data = get(request, APPLICATIONS_URL + str(pk) + EXISTING_PARTIES_URL + params)
    return data.json(), data.status_code


# Consignee Documents
def get_consignee_document(request, pk):
    data = get(request, APPLICATIONS_URL + pk + CONSIGNEE_DOCUMENT_URL)
    return data.json(), data.status_code


def post_consignee_document(request, pk, json):
    data = post(request, APPLICATIONS_URL + pk + CONSIGNEE_DOCUMENT_URL, json)
    return data.json(), data.status_code


def delete_consignee_document(request, pk):
    data = delete(request, APPLICATIONS_URL + pk + CONSIGNEE_DOCUMENT_URL)
    return data.status_code


# Additional Documents
def post_additional_document(request, pk, json):
    data = post(request, APPLICATIONS_URL + pk + ADDITIONAL_DOCUMENT_URL, json)
    return data.json(), data.status_code


def get_additional_documents(request, pk):
    data = get(request, APPLICATIONS_URL + pk + ADDITIONAL_DOCUMENT_URL)
    return data.json(), data.status_code


def get_additional_document(request, pk, doc_pk):
    data = get(request, APPLICATIONS_URL + pk + ADDITIONAL_DOCUMENT_URL + str(doc_pk) + "/")
    return data.json(), data.status_code


def delete_additional_party_document(request, pk, doc_pk):
    data = delete(request, APPLICATIONS_URL + pk + ADDITIONAL_DOCUMENT_URL + str(doc_pk) + "/")
    return data.status_code


def delete_application_preexisting_good(request, good_on_application_pk):
    response = delete(request, APPLICATIONS_URL + "good-on-application/" + good_on_application_pk)
    return response.status_code


# Case related
def get_case_notes(request, pk):
    data = get(request, CASES_URL + pk + CASE_NOTES_URL)
    return data.json()


def post_application_case_notes(request, pk, json):
    data = post(request, CASES_URL + pk + CASE_NOTES_URL, json)
    return data.json(), data.status_code


def get_ecju_query(request, pk, query_pk):
    data = get(request, CASES_URL + pk + ECJU_QUERIES_URL + query_pk).json()["ecju_query"]
    return data


def put_ecju_query(request, pk, query_pk, json):
    data = put(request, CASES_URL + pk + ECJU_QUERIES_URL + query_pk + "/", json)
    return data.json(), data.status_code


def get_application_ecju_queries(request, pk):
    data = get(request, CASES_URL + pk + ECJU_QUERIES_URL).json()["ecju_queries"]

    open_queries = [x for x in data if not x["response"]]
    closed_queries = [x for x in data if x["response"]]

    return open_queries, closed_queries


def get_application_generated_documents(request, pk):
    data = get(request, APPLICATIONS_URL + pk + GENERATED_DOCUMENTS_URL).json()["generated_documents"]
    return data


def get_generated_document(request, pk, doc_pk):
    data = get(request, APPLICATIONS_URL + pk + GENERATED_DOCUMENTS_URL + str(doc_pk) + "/")
    return data.json(), data.status_code


def get_status_properties(request, status):
    data = get(request, STATUS_PROPERTIES_URL + status)
    return data.json(), data.status_code


def set_application_status(request, pk, status):
    json = {"status": status}
    data = put(request, APPLICATIONS_URL + str(pk) + MANAGE_STATUS_URL, json)
    return data.json(), data.status_code


def add_document_data(request):
    files = request.FILES.getlist("file")
    if not files:
        return None, "No files attached"
    if len(files) != 1:
        return None, "Multiple files attached"

    file = files[0]
    try:
        original_name = file.original_name
    except Exception:  # noqa
        original_name = file.name

    data = {
        "name": original_name,
        "s3_key": file.name,
        "size": int(file.size // 1024) if file.size else 0,  # in kilobytes
    }
    if "description" in request.POST:
        data["description"] = request.POST.get("description")

    return data, None


# Stream file
def generate_file(result):
    for chunk in iter(lambda: result["Body"].read(STREAMING_CHUNK_SIZE), b""):
        yield chunk


def download_document_from_s3(s3_key, original_file_name):
    s3 = s3_client()
    s3_response = s3.get_object(Bucket=AWS_STORAGE_BUCKET_NAME, Key=s3_key)
    _kwargs = {}
    if s3_response.get("ContentType"):
        _kwargs["content_type"] = s3_response["ContentType"]
    response = StreamingHttpResponse(generate_file(s3_response), **_kwargs)
    response["Content-Disposition"] = f'attachment; filename="{original_file_name}"'
    return response


# Goods Types
def get_goods_type(request, app_pk, good_pk):
    data = get(request, APPLICATIONS_URL + app_pk + GOODSTYPE_URL + good_pk + "/")
    return data.json(), data.status_code


def post_goods_type(request, app_pk, json):
    data = post(request, APPLICATIONS_URL + str(app_pk) + GOODSTYPES_URL, json)
    return data.json(), data.status_code


def delete_goods_type(request, app_pk, good_pk):
    data = delete(request, APPLICATIONS_URL + app_pk + GOODSTYPE_URL + good_pk + "/")
    return data.status_code


def put_goods_type_countries(request, app_pk, json):
    data = put(request, APPLICATIONS_URL + app_pk + GOODSTYPE_URL + GOODSTYPE_COUNTRY_URL, json)
    return data.json(), data.status_code


def get_goods_type_document(request, pk, good_pk):
    data = get(request, APPLICATIONS_URL + pk + GOODSTYPE_URL + str(good_pk) + DOCUMENT_URL)
    return data.json(), data.status_code


def post_goods_type_document(request, pk, good_pk, json):
    data = post(request, APPLICATIONS_URL + pk + GOODSTYPE_URL + str(good_pk) + DOCUMENT_URL, json)
    return data.json(), data.status_code


def delete_goods_type_document(request, pk, good_pk):
    data = delete(request, APPLICATIONS_URL + pk + GOODSTYPE_URL + str(good_pk) + DOCUMENT_URL)
    return data.status_code


# Activity
def get_activity(request, pk):
    data = get(request, CASES_URL + pk + ACTIVITY_URL)
    return data.json()["activity"]
