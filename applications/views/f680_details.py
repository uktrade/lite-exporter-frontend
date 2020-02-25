from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from applications.forms.f680_details import f680_details_form
from applications.services import get_application, put_application
from lite_forms.views import SingleFormView


class F680Details(SingleFormView):
    # def get(self, request, **kwargs):
    #     application_id = str(kwargs["pk"])
    #     application = get_application(request, application_id)
    #
    #     return render(request, "applications/f680-details.html", {"application": application})
    def init(self, request, **kwargs):
        application_id = str(kwargs["pk"])
        application = get_application(request, application_id)

        print("\n")

        print("application", application)

        print("\n")

        self.data = {}
        self.form = f680_details_form(self.object_pk)
        self.action = put_application

        self.success_url = reverse_lazy("applications:task_list", kwargs={"pk": self.object_pk})
