from http import HTTPStatus
from inspect import signature
from typing import List

from django.urls import reverse_lazy
from s3chunkuploader.file_handler import S3FileUploadHandler

from applications.forms.questions import questions_forms
from applications.helpers.reverse_documents import document_switch
from applications.services import post_application_questions, get_application_questions, add_document_data
from applications.views.documents import get_upload_page
from lite_content.lite_exporter_frontend import strings
from lite_forms.views import SummaryListFormView


def questions_action(request, pk, json):
    return post_application_questions(request, pk, json)


class QuestionsFormView(SummaryListFormView):
    def init(self, request, **kwargs):
        self.object_pk = str(kwargs["pk"])
        self.data = get_application_questions(request, self.object_pk)
        self.forms = questions_forms()
        self.action = questions_action
        self.success_url = reverse_lazy("applications:task_list", kwargs={"pk": self.object_pk})
        self.summary_list_title = "Additional information"
        self.summary_list_notice_title = ""
        self.summary_list_notice_text = ""
        self.summary_list_button = "Save and return"

    def post_form_4(self, request, **kwargs):

        data, error = add_document_data(request)
        if error:
            return {"electronic_warfare_requirement_attachment": [error]}

        uploaded = False

        """
        Upload to API HERE
        """
        if uploaded:
            return {"electronic_warfare_requirement_attachment": [
                strings.applications.AttachDocumentPage.UPLOAD_FAILURE_ERROR
            ]}


"""
        draft_id = str(kwargs["pk"])
        form = get_upload_page(request.path, draft_id)
        self.request.upload_handlers.insert(0, S3FileUploadHandler(request))

        logging.info(self.request)
        data, error = add_document_data(request)

        if error:
            return form_page(request, form, extra_data={"draft_id": draft_id}, errors={"documents": [error]})

        action = document_switch(request.path)["attach"]
        if len(signature(action).parameters) == 3:
            _, status_code = action(request, draft_id, data)
            if status_code == HTTPStatus.CREATED:
                return get_homepage(request, draft_id)
        else:
            _, status_code = action(request, draft_id, kwargs["obj_pk"], data)
            if status_code == HTTPStatus.CREATED:
                return get_homepage(request, draft_id, kwargs["obj_pk"])

        return error_page(request, strings.applications.AttachDocumentPage.UPLOAD_FAILURE_ERROR)
"""
