import ast

from django.contrib.humanize.templatetags.humanize import intcomma
from django.urls import reverse_lazy

from applications.forms.questions import questions_forms
from applications.services import put_application, get_application
from lite_content.lite_exporter_frontend import applications
from lite_content.lite_exporter_frontend import generic
from lite_forms.views import SummaryListFormView


def questions_action(request, pk, json):
    def to_bool(val):
        if isinstance(val, bool):
            return val
        elif isinstance(val, str):
            if val.lower() == "false":
                return False
            elif val.lower() == "true":
                return True
        return False

    if to_bool(json.get("expedited", False)):
        if "year" in json and "month" in json and "day" in json:
            json["expedited_date"] = f"{json['year']}-{json['month']}-{json['day']}"

    else:
        if "expedited_date" in json:
            del json["expedited_date"]

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
    return put_application(request, pk, json)


class AdditionalInformationFormView(SummaryListFormView):
    def init(self, request, **kwargs):
        self.object_pk = str(kwargs["pk"])
        self.data = self.get_additional_information(request, self.object_pk)
        self.forms = questions_forms()
        self.action = questions_action
        self.success_url = reverse_lazy("applications:task_list", kwargs={"pk": self.object_pk})
        self.summary_list_title = applications.F680ClearanceTaskList.ADDITIONAL_INFORMATION
        self.summary_list_notice_title = ""
        self.summary_list_notice_text = ""
        self.summary_list_button = generic.SAVE_AND_RETURN
        self.validate_only_until_final_submission = False

    def prettify_data(self, data):
        data = super().prettify_data(data)
        if "value" in data and data["value"]:
            data["value"] = f"£{intcomma(data['value'])}"
        return data

    @staticmethod
    def get_additional_information(request, application_id):
        fields = [
            "expedited",
            "expedited_date",
            "expedited_description",
            "foreign_technology",
            "foreign_technology_description",
            "locally_manufactured",
            "locally_manufactured_description",
            "mtcr_type",
            "electronic_warfare_requirement",
            "uk_service_equipment",
            "uk_service_equipment_description",
            "uk_service_equipment_type",
            "prospect_value",
        ]
        application = get_application(request, application_id)
        return {
            field: application[field] for field in fields if application.get(field) is not None
        }
