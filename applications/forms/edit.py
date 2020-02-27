from applications.components import back_to_task_list
from lite_content.lite_exporter_frontend import applications, generic
from lite_forms.components import Form, TextInput, Option, Checkboxes, RadioButtons
from lite_forms.helpers import conditional


def reference_name_form(application_id=None):
    return Form(
        title=applications.InitialApplicationQuestionsForms.ReferenceNameQuestion.TITLE,
        description=applications.InitialApplicationQuestionsForms.ReferenceNameQuestion.DESCRIPTION,
        questions=[TextInput(name="name"),],
        back_link=back_to_task_list(application_id),
        default_button_name=conditional(application_id, generic.SAVE_AND_RETURN, generic.CONTINUE),
    )


def goods_categories(application_id=None):
    return Form(
        title=applications.GoodsCategories.TITLE,
        description=applications.GoodsCategories.DESCRIPTION,
        questions=[
            Checkboxes(
                name="goods_categories[]",
                options=[
                    Option(key="anti_piracy", value="Anti-piracy",),
                    Option(key="maritime_anti_piracy", value="Maritime anti-piracy",),
                    Option(key="firearms", value="Firearms",),
                    Option(key="incorporated_goods", value="Incorporated goods",),
                ],
            )
        ],
        back_link=back_to_task_list(application_id),
        default_button_name=conditional(application_id, generic.SAVE_AND_RETURN, generic.CONTINUE),
    )


def told_by_an_official_form(application_id=None):
    return Form(
        title="Have you been informed under an ‘end use control’ that you need to apply for a licence?",
        description="An end use control is an official letter or email from Border Force or HMRC.",
        questions=[
            RadioButtons(
                name="have_you_been_informed",
                options=[
                    Option(key="yes",
                           value="Yes",
                           components=[
                               TextInput(
                                   title="Reference number",
                                   description="The reference number is on the official letter or email.",
                                   name="reference_number_on_information_form",
                                   optional=True,
                               ),
                           ]),
                    Option(key="no",
                           value="No"),
                ],
            ),
        ],
        back_link=back_to_task_list(application_id),
        default_button_name=conditional(application_id, generic.SAVE_AND_RETURN, generic.CONTINUE),
    )
