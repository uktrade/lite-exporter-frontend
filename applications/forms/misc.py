from applications.components import back_to_task_list
from lite_forms.components import Form, TextInput, Option, Checkboxes
from lite_content.lite_exporter_frontend.applications import InitialApplicationQuestionsForms


def reference_name_form(application_id):
    return Form(
        title="Name the application",
        description="Give the application a reference name so you can refer back to it when needed.",
        questions=[TextInput(name="name", title=InitialApplicationQuestionsForms.OpeningQuestion.LABEL),],
        back_link=back_to_task_list(application_id),
    )


def goods_categories(application_id: None):
    return Form(
        title="Does your application include?",
        description="",
        questions=[
            Checkboxes(
                name="goods_categories[]",
                options=[
                    Option(
                        key="anti_piracy",
                        value="Anti-piracy",
                        description="",
                    ),
                    Option(
                        key="maritime_anti_piracy",
                        value="Maritime anti-piracy",
                        description="",
                    ),
                    Option(
                        key="firearms",
                        value="Firearms",
                        description="",
                    ),
                    Option(
                        key="incorporated_goods",
                        value="Incorporated goods",
                        description="",
                    )
                ]
            )
        ],
        back_link=back_to_task_list(application_id),
    )
