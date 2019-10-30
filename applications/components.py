from django.urls import reverse_lazy
from lite_forms.components import BackLink, Label


def back_to_task_list(application_id):
    return BackLink('Back to task list', reverse_lazy('applications:edit', kwargs={'pk': application_id}))


def footer_label(application_id):
    return Label('Or <a class="govuk-link" href="' +
                 reverse_lazy('applications:edit', kwargs={'pk': str(application_id)}) +
                 '">Or return to the task list</a>')
