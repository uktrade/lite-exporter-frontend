from django.urls import reverse_lazy

from applications.services import post_applications
from apply_for_a_licence.forms import licence_type, initial_questions
from lite_forms.views import SingleFormView, MultiFormView


class LicenceType(SingleFormView):
    def init(self, request, **kwargs):
        self.form = licence_type()
        # TODO Change to validator
        self.action = post_applications

    def get_success_url(self):
        # TODO redirect depending on what is chose
        return reverse_lazy("applications:task_list", kwargs={"pk": pk})


class InitialQuestions(MultiFormView):
    def init(self, request, **kwargs):
        self.forms = initial_questions(None)
        self.action = post_applications

    def on_submission(self, request, **kwargs):
        self.forms = initial_questions(request.POST.copy().get("application_type"))

    def get_success_url(self):
        pk = self.get_validated_data()["id"]
        return reverse_lazy("applications:task_list", kwargs={"pk": pk})
