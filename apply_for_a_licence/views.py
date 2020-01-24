from django.urls import reverse_lazy

from applications.services import post_applications
from apply_for_a_licence.forms import opening_question, export_licence_questions
from apply_for_a_licence.validators import validate_opening_question
from lite_forms.views import SingleFormView, MultiFormView


class LicenceType(SingleFormView):
    def init(self, request, **kwargs):
        self.form = opening_question()
        self.action = validate_opening_question

    def get_success_url(self):
        pk = self.get_validated_data()["id"]
        return reverse_lazy("applications:task_list", kwargs={"pk": pk})


class ExportLicenceQuestions(MultiFormView):
    def init(self, request, **kwargs):
        self.forms = export_licence_questions(None)
        self.action = post_applications

    def on_submission(self, request, **kwargs):
        self.forms = export_licence_questions(request.POST.copy().get("application_type"))

    def get_success_url(self):
        pk = self.get_validated_data()["id"]
        return reverse_lazy("applications:task_list", kwargs={"pk": pk})


class MODClearanceQuestions(MultiFormView):
    def init(self, request, **kwargs):
        self.forms = export_licence_questions(None)
        self.action = post_applications

    def on_submission(self, request, **kwargs):
        self.forms = export_licence_questions(request.POST.copy().get("application_type"))

    def get_success_url(self):
        pk = self.get_validated_data()["id"]
        return reverse_lazy("applications:task_list", kwargs={"pk": pk})
