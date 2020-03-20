import ast

from django.contrib.humanize.templatetags.humanize import intcomma
from django.urls import reverse_lazy

from applications.forms.questions import questions_forms
from applications.services import post_application_questions, get_application_questions
from lite_content.lite_exporter_frontend import applications
from lite_content.lite_exporter_frontend import generic
from lite_forms.views import SummaryListFormView


def questions_action(request, pk, json):
    if json.get("expedited", False):
        if "year" in json and "month" in json and "day" in json:
            json["expedited_date"] = f"{json['year']}-{json['month']}-{json['day']}"

    empty_keys = []
    for key in json:
        try:
            # Try to cast to dict if str in order to handle key|value pairs
            json[key] = ast.literal_eval(json[key])
            if isinstance(json[key], dict) and "key" in json[key]:
                json[key] = json[key]["key"]
        except (ValueError, SyntaxError):
            pass
        if not isinstance(json[key], bool) and not json[key]:
            empty_keys.append(key)
    for key in empty_keys:
        del json[key]

    return post_application_questions(request, pk, json)


class QuestionsFormView(SummaryListFormView):
    def init(self, request, **kwargs):
        self.object_pk = str(kwargs["pk"])
        self.data = get_application_questions(request, self.object_pk)
        self.forms = questions_forms()
        self.action = questions_action
        self.success_url = reverse_lazy("applications:task_list", kwargs={"pk": self.object_pk})
        self.summary_list_title = applications.F680ClearanceTaskList.ADDITIONAL_INFORMATION
        self.summary_list_notice_title = ""
        self.summary_list_notice_text = applications.F680Questions
        self.summary_list_button = generic.SAVE_AND_RETURN

    def prettify_data(self, data):
        data = super().prettify_data(data)
        if "value" in data and data["value"]:
            data["value"] = f"£{intcomma(data['value'])}"
        return data
