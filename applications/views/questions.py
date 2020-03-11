from django.urls import reverse_lazy

from applications.forms.questions import questions_forms
from applications.services import post_application_questions, get_application_questions
from lite_forms.views import SummaryListFormView


def questions_action(request, pk, json):
    return post_application_questions(request, pk, json)


class QuestionsFormView(SummaryListFormView):
    def init(self, request, **kwargs):
        self.object_pk = str(kwargs["pk"])
        self.data = get_application_questions(request, self.object_pk)
        from pprint import pprint
        pprint(self.data)
        self.forms = questions_forms()
        self.action = questions_action
        self.success_url = reverse_lazy("applications:task_list", kwargs={"pk": self.object_pk})
        self.summary_list_title = "Additional information"
        self.summary_list_notice_title = ""
        self.summary_list_notice_text = ""
        self.summary_list_button = "Save and return"
