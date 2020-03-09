from django.urls import reverse_lazy

from applications.forms.end_use_details import end_use_details_form
from applications.services import put_application, get_application
from conf.constants import STANDARD
from lite_forms.views import MultiFormView, SummaryListFormView


class EndUseDetails(SummaryListFormView):

    def init(self, request, **kwargs):
        self.draft_pk = str(kwargs["pk"])
        application = get_application(request, self.object_pk)
        is_application_type_standard = application["case_type"]["sub_type"]["key"] == STANDARD
        self.forms = end_use_details_form(is_application_type_standard)
        self.action = put_application