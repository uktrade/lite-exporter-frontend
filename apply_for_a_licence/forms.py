from django.urls import reverse_lazy

from conf.constants import STANDARD_LICENCE, OPEN_LICENCE
from lite_content.lite_exporter_frontend import strings, generic
from lite_forms.components import RadioButtons, Form, DetailComponent, TextInput, Option, FormGroup, Breadcrumbs, \
    BackLink
from lite_forms.helpers import conditional


def licence_type():
    return Form(
        title="What type of licence do you want to apply for?",
        description="Easy to find description here",
        questions=[
            RadioButtons(
                name="licence_type",
                options=[
                    Option(
                        key="export", value="Export Licence", description="Exporting goods from UK to somewhere else"
                    ),
                    Option(
                        key="transhipment",
                        value="Transhipment",
                        description="Shipping something from abroad through the UK, within 30 days, on to another destination abroad",
                    ),
                    Option(
                        key="trade_control",
                        value="Trade Control",
                        description="Arranging or brokering the sale or movements of controlled goods (the goods may not be located here)",
                    ),
                    Option(
                        key="mod",
                        value="MOD Clearance",
                        description="Sharing information (F680), exhibition clearance or gifting",
                    ),
                ],
            )
        ],
        default_button_name="Continue",
        back_link=Breadcrumbs([
            BackLink(generic.SERVICE_NAME, reverse_lazy("core:hub")),
            BackLink("Apply for a licence", ""),
        ])
    )


def initial_questions(application_type):
    return FormGroup(
        [
            Form(
                title=strings.applications.InitialApplicationQuestionsForms.WHICH_EXPORT_LICENCE_DO_YOU_WANT_TITLE,
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
                    DetailComponent(
                        strings.applications.InitialApplicationQuestionsForms.HELP_WITH_CHOOSING_A_LICENCE,
                        strings.applications.InitialApplicationQuestionsForms.HELP_WITH_CHOOSING_A_LICENCE_CONTENT,
                    ),
                ],
                default_button_name=strings.CONTINUE,
            ),
            Form(
                title=strings.applications.InitialApplicationQuestionsForms.ENTER_A_REFERENCE_NAME_TITLE,
                description=strings.applications.InitialApplicationQuestionsForms.ENTER_A_REFERENCE_NAME_DESCRIPTION,
                questions=[TextInput(name="name"),],
                default_button_name=strings.CONTINUE,
            ),
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
