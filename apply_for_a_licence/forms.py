from django.urls import reverse_lazy

from conf.constants import STANDARD_LICENCE, OPEN_LICENCE
from lite_content.lite_exporter_frontend import strings, generic
from lite_forms.components import (
    RadioButtons,
    Form,
    DetailComponent,
    TextInput,
    Option,
    FormGroup,
    Breadcrumbs,
    BackLink,
)
from lite_forms.helpers import conditional


def reference_name_question():
    return Form(
        title=strings.applications.InitialApplicationQuestionsForms.ENTER_A_REFERENCE_NAME_TITLE,
        description=strings.applications.InitialApplicationQuestionsForms.ENTER_A_REFERENCE_NAME_DESCRIPTION,
        questions=[TextInput(name="name"), ],
        default_button_name=strings.CONTINUE,
    )


def opening_question():
    return Form(title="What type of licence do you want to apply for?",
                questions=[
                    RadioButtons(
                        name="licence_type",
                        options=[
                            Option(
                                key="export_licence",
                                value="Export Licence",
                                description="Select if you’re sending products produced in the UK to another country"
                            ),
                            Option(
                                key="export_licence",
                                value="Transhipment licence",
                                description="Select if you’re shipping something from overseas through the UK on to another country. If the products will be in the UK for 31 days or more, apply for an export licence",
                            ),
                            Option(
                                key="export_licence",
                                value="Trade control licence ",
                                description="Select if you’re arranging or brokering the sale or movement of controlled products located overseas",
                            ),
                            Option(
                                key="mod",
                                value="MOD clearance",
                                description="Select if you need to share information, go to an exhibition or gifting products",
                            ),
                        ],
                    ),
                    DetailComponent(
                        strings.applications.InitialApplicationQuestionsForms.HELP_WITH_CHOOSING_A_LICENCE,
                        strings.applications.InitialApplicationQuestionsForms.HELP_WITH_CHOOSING_A_LICENCE_CONTENT,
                    ),
                ],
                default_button_name=strings.CONTINUE,
                back_link=Breadcrumbs([
                    BackLink(generic.SERVICE_NAME, reverse_lazy("core:hub")),
                    BackLink("Apply for a licence", ""),
                ]))


def export_licence_questions(application_type):
    return FormGroup(
        [
            Form(title=strings.applications.InitialApplicationQuestionsForms.WHICH_EXPORT_LICENCE_DO_YOU_WANT_TITLE,
                 description=strings.applications.InitialApplicationQuestionsForms.WHICH_EXPORT_LICENCE_DO_YOU_WANT_DESCRIPTION,
                 questions=[
                     RadioButtons(
                         name="application_type",
                         options=[
                             Option(
                                 key=STANDARD_LICENCE,
                                 value=strings.applications.InitialApplicationQuestionsForms.STANDARD_LICENCE,
                                 description=strings.applications.InitialApplicationQuestionsForms.STANDARD_LICENCE_DESCRIPTION,
                             ),
                             Option(
                                 key=OPEN_LICENCE,
                                 value=strings.applications.InitialApplicationQuestionsForms.OPEN_LICENCE,
                                 description=strings.applications.InitialApplicationQuestionsForms.OPEN_LICENCE_DESCRIPTION,
                             ),
                         ],
                     ),
                 ],
                 default_button_name=strings.CONTINUE, ),
            reference_name_question(),
            Form(
                title=strings.applications.InitialApplicationQuestionsForms.TEMPORARY_OR_PERMANENT_TITLE,
                description=strings.applications.InitialApplicationQuestionsForms.TEMPORARY_OR_PERMANENT_DESCRIPTION,
                questions=[
                    RadioButtons(
                        name="export_type",
                        options=[
                            Option("temporary", strings.applications.InitialApplicationQuestionsForms.TEMPORARY),
                            Option("permanent", strings.applications.InitialApplicationQuestionsForms.PERMANENT),
                        ],
                    ),
                ],
                default_button_name=strings.CONTINUE
                if application_type == STANDARD_LICENCE
                else strings.SAVE_AND_CONTINUE,
            ),
            conditional(
                application_type != OPEN_LICENCE,
                Form(
                    title=strings.applications.InitialApplicationQuestionsForms.HAVE_YOU_BEEN_INFORMED_TITLE,
                    description=strings.applications.InitialApplicationQuestionsForms.HAVE_YOU_BEEN_INFORMED_DESCRIPTION,
                    questions=[
                        RadioButtons(
                            name="have_you_been_informed",
                            options=[
                                Option("yes", strings.YES, show_pane="pane_reference_number_on_information_form"),
                                Option("no", strings.NO),
                            ],
                            classes=["govuk-radios--inline"],
                        ),
                        TextInput(
                            title=strings.applications.InitialApplicationQuestionsForms.WHAT_WAS_THE_REFERENCE_CODE_TITLE,
                            description=strings.applications.InitialApplicationQuestionsForms.WHAT_WAS_THE_REFERENCE_CODE_DESCRIPTION,
                            name="reference_number_on_information_form",
                            optional=True,
                        ),
                    ],
                    default_button_name=strings.SAVE_AND_CONTINUE,
                ),
            ),
        ]
    )


def MOD_questions():
    return FormGroup([
        Form(title="What are you mod applying for?",
             description="mod description",
             questions=[
                 RadioButtons(
                     name="type",
                     options=[
                         Option(
                             key="permission",
                             value="Permission to share information",
                             description="",
                         ),
                         Option(
                             key="exhibition_clearance",
                             value="Exhibition clearance",
                             description="",
                         ),
                         Option(
                             key="gifting_clearance",
                             value="Gifting clearance",
                             description="",
                         ),
                     ],
                 ),
             ],
             default_button_name=strings.CONTINUE, ),
        reference_name_question(),
    ])
