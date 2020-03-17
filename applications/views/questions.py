from http import HTTPStatus

from django.contrib.humanize.templatetags.humanize import intcomma
from django.urls import reverse_lazy

from applications.forms.questions import questions_forms
from applications.services import (
    post_application_questions,
    get_application_questions,
    add_document_data,
    post_additional_document,
)
from lite_content.lite_exporter_frontend import strings
from lite_forms.views import SummaryListFormView


def questions_action(request, pk, json):
    if json.get("expedited", False):
        if "year" in json and "month" in json and "day" in json:
            json["expedited_date"] = f"{json['year']}-{json['month']}-{json['day']}"
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
        draft_id = str(kwargs["pk"])
        if request.POST.get("electronic_warfare_requirement", False):
            data, error = add_document_data(request)
            if error:
                return {}, {"documents": [error]}

            action = post_additional_document
            data, status_code = action(request, draft_id, data)

            if status_code == HTTPStatus.CREATED:
                return {"electronic_warfare_requirement_attachment": data["document"]["id"]}, None

            return {}, {"errors": strings.applications.AttachDocumentPage.UPLOAD_FAILURE_ERROR}
        return {}, None

    def prettify_data(self, data):
        data = super().prettify_data(data)
        if "question_7" in data and data["question_7"]:
            data["question_7"] = "£" + intcomma(data["question_7"])
        return data
