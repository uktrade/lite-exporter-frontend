from django.urls import reverse_lazy

from applications.forms.temporary_export_details import temporary_export_details_form
from applications.helpers.date_fields import date_splitter
from applications.services import get_application, put_temporary_export_details
from lite_content.lite_exporter_frontend import generic
from lite_content.lite_exporter_frontend.applications import TemporaryExportDetails as strings
from lite_forms.views import SummaryListFormView


class TemporaryExportDetails(SummaryListFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        application = get_application(request, self.object_pk)
        self.forms = temporary_export_details_form()
        self.action = put_temporary_export_details
        self.data = self._parse_temporary_export_details(application)
        self.success_url = reverse_lazy("applications:task_list", kwargs={"pk": self.object_pk})
        self.summary_list_title = strings.SummaryList.TITLE
        self.summary_list_notice_title = ""
        self.summary_list_notice_text = ""
        self.summary_list_button = generic.SAVE_AND_RETURN
        self.validate_only_until_final_submission = False

    def get_validated_data(self):
        data = super().get_validated_data()
        # to ensure date is changed and displayed on the summary list
        if data.get("year") and data.get("month") and data.get("day"):
            data["proposed_return_date"] = f"{data['year']}-{str(data['month']).zfill(2)}-{str(data['day']).zfill(2)}"
        return data

    def prettify_data(self, data):
        data = super().prettify_data(data)
        return data

    @staticmethod
    def _parse_temporary_export_details(application):

        temporary_export_details_text_fields = [
            "temp_export_details",
            "temp_direct_control_details",
        ]

        data = {}

        if application.get("is_temp_direct_control") is not None:
            data["is_temp_direct_control"] = application.get("is_temp_direct_control")

        for temp_export_detail in temporary_export_details_text_fields:
            application_temp_export_detail = application.get(temp_export_detail)
            if application_temp_export_detail:
                data[temp_export_detail] = application_temp_export_detail

        proposed_return_date = application.get("proposed_return_date")
        if proposed_return_date:
            date_components = date_splitter(proposed_return_date, "-")
            data["year"] = date_components["year"]
            data["month"] = date_components["month"]
            data["day"] = date_components["day"]

        return data
