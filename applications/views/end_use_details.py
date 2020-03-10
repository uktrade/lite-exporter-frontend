from django.urls import reverse_lazy

from applications.forms.end_use_details import end_use_details_form
from applications.services import put_application, get_application
from conf.constants import STANDARD
from lite_forms.views import SummaryListFormView


class EndUseDetails(SummaryListFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        application = get_application(request, self.object_pk)
        is_application_type_standard = application.sub_type == STANDARD
        self.forms = end_use_details_form(is_application_type_standard)
        self.action = put_application
        self.data = self._parse_end_use_details(application)
        self.success_url = reverse_lazy("applications:task_list", kwargs={"pk": self.object_pk})
        self.validate_only_until_final_submission = True
        self.summary_list_title = "WMD end use summary list"
        self.summary_list_notice_title = ""
        self.summary_list_notice_text = ""
        self.summary_list_button = "Save and continue"

    def _parse_end_use_details(self, application):
        end_use_detail_questions = [
            "is_military_end_use_controls",
            "is_informed_wmd",
            "is_suspected_wmd",
            "is_eu_military",
        ]
        end_use_detail_references = [
            "military_end_use_controls_ref",
            "informed_wmd_ref",
            "suspected_wmd_ref",
            "eu_military_ref",
        ]

        data = {}
        for end_use_question in end_use_detail_questions:
            end_use_question_answer = application.get(end_use_question)
            if end_use_question_answer:
                data[end_use_question] = end_use_question_answer["key"]
        for ref_end_use_field in end_use_detail_references:
            data[ref_end_use_field] = application.get(ref_end_use_field)
        return data
