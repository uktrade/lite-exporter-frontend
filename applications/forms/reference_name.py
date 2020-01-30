from applications.components import back_to_task_list
from lite_forms.components import Form, TextInput
from lite_content.lite_exporter_frontend.applications import InitialApplicationQuestionsForms


def reference_name_form(application_id):
    return Form(
        title="Name the application",
        description="Give the application a reference name so you can refer back to it when needed.",
        questions=[TextInput(name="name", title=InitialApplicationQuestionsForms.OpeningQuestion.LABEL),],
        back_link=back_to_task_list(application_id),
    )
