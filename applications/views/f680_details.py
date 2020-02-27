from django.urls import reverse_lazy

from applications.forms.f680_details import f680_details_form
from applications.services import put_application
from lite_forms.views import SingleFormView


class F680Details(SingleFormView):
    def init(self, request, **kwargs):
        self.form = f680_details_form(self.object_pk)
        self.action = put_application
        self.object_pk = str(kwargs["pk"])
        self.success_url = reverse_lazy("applications:task_list", kwargs={"pk": self.object_pk})
