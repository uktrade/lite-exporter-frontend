from django.urls import reverse_lazy

from applications.forms.edit import goods_categories, reference_name_form, told_by_an_official_form
from conf.constants import CaseTypes
from lite_content.lite_exporter_frontend import generic
from lite_content.lite_exporter_frontend.applications import (
    InitialApplicationQuestionsForms,
    ExportLicenceQuestions,
    MODQuestions,
    TranshipmentQuestions,
    TradeControlLicenceQuestions,
)
from lite_forms.components import (
    Form,
    RadioButtons,
    Option,
    Breadcrumbs,
    BackLink,
    FormGroup,
    DetailComponent,
    Label,
    TextInput,
    HiddenField,
)
from lite_forms.helpers import conditional


def opening_question():
    return Form(
        title=InitialApplicationQuestionsForms.OpeningQuestion.TITLE,
        description=InitialApplicationQuestionsForms.OpeningQuestion.DESCRIPTION,
        questions=[
            RadioButtons(
                name="licence_type",
                options=[
                    Option(
                        key="export_licence",
                        value=InitialApplicationQuestionsForms.OpeningQuestion.LicenceTypes.EXPORT_LICENCE_TITLE,
                        description=InitialApplicationQuestionsForms.OpeningQuestion.LicenceTypes.EXPORT_LICENCE_DESCRIPTION,
                    ),
                    Option(
                        key="transhipment",
                        value=InitialApplicationQuestionsForms.OpeningQuestion.LicenceTypes.TRANSHIPMENT_LICENCE_TITLE,
                        description=InitialApplicationQuestionsForms.OpeningQuestion.LicenceTypes.TRANSHIPMENT_LICENCE_DESCRIPTION,
                    ),
                    Option(
                        key="trade_control_licence",
                        value=InitialApplicationQuestionsForms.OpeningQuestion.LicenceTypes.TRADE_CONTROL_LICENCE_TITLE,
                        description=InitialApplicationQuestionsForms.OpeningQuestion.LicenceTypes.TRADE_CONTROL_LICENCE_DESCRIPTION,
                    ),
                    Option(
                        key="mod",
                        value=InitialApplicationQuestionsForms.OpeningQuestion.LicenceTypes.MOD_CLEARANCE_TITLE,
                        description=InitialApplicationQuestionsForms.OpeningQuestion.LicenceTypes.MOD_CLEARANCE_DESCRIPTION,
                    ),
                ],
            ),
        ],
        default_button_name=generic.CONTINUE,
        back_link=Breadcrumbs(
            [
                BackLink(generic.SERVICE_NAME, reverse_lazy("core:home")),
                BackLink(InitialApplicationQuestionsForms.OpeningQuestion.BREADCRUMB, ""),
            ]
        ),
    )


def export_licence_questions(application_type):
    return FormGroup(
        [
            Form(
                title=ExportLicenceQuestions.ExportLicenceQuestion.TITLE,
                description=ExportLicenceQuestions.ExportLicenceQuestion.DESCRIPTION,
                questions=[
                    RadioButtons(
                        name="application_type",
                        options=[
                            Option(
                                key=CaseTypes.SIEL,
                                value=ExportLicenceQuestions.ExportLicenceQuestion.STANDARD_LICENCE,
                                description=ExportLicenceQuestions.ExportLicenceQuestion.STANDARD_LICENCE_DESCRIPTION,
                            ),
                            Option(
                                key=CaseTypes.OIEL,
                                value=ExportLicenceQuestions.ExportLicenceQuestion.OPEN_LICENCE,
                                description=ExportLicenceQuestions.ExportLicenceQuestion.OPEN_LICENCE_DESCRIPTION,
                            ),
                        ],
                    ),
                    DetailComponent(
                        InitialApplicationQuestionsForms.OpeningQuestion.HELP_WITH_CHOOSING_A_LICENCE,
                        InitialApplicationQuestionsForms.OpeningQuestion.HELP_WITH_CHOOSING_A_LICENCE_CONTENT,
                    ),
                ],
                default_button_name=generic.CONTINUE,
                back_link=BackLink(
                    ExportLicenceQuestions.ExportLicenceQuestion.BACK, reverse_lazy("apply_for_a_licence:start")
                ),
            ),
            reference_name_form(),
            Form(
                title=ExportLicenceQuestions.ExportType.TITLE,
                description=ExportLicenceQuestions.ExportType.DESCRIPTION,
                questions=[
                    RadioButtons(
                        name="export_type",
                        options=[
                            Option("temporary", ExportLicenceQuestions.ExportType.TEMPORARY),
                            Option("permanent", ExportLicenceQuestions.ExportType.PERMANENT),
                        ],
                    ),
                ],
                default_button_name=generic.CONTINUE
                if application_type == CaseTypes.SIEL
                else generic.SAVE_AND_CONTINUE,
            ),
            *conditional(application_type == CaseTypes.SIEL, [goods_categories(), told_by_an_official_form()], []),
        ]
    )


def trade_control_licence_questions():
    return FormGroup(
        [
            Form(
                title=TradeControlLicenceQuestions.TradeControlLicenceQuestion.TITLE,
                description=TradeControlLicenceQuestions.TradeControlLicenceQuestion.DESCRIPTION,
                questions=[
                    RadioButtons(
                        name="application_type",
                        options=[
                            Option(
                                key=CaseTypes.SICL,
                                value=TradeControlLicenceQuestions.TradeControlLicenceQuestion.STANDARD_LICENCE,
                                description=TradeControlLicenceQuestions.TradeControlLicenceQuestion.STANDARD_LICENCE_DESCRIPTION,
                            ),
                            Option(
                                key=CaseTypes.OICL,
                                value=TradeControlLicenceQuestions.TradeControlLicenceQuestion.OPEN_LICENCE,
                                description=TradeControlLicenceQuestions.TradeControlLicenceQuestion.OPEN_LICENCE_DESCRIPTION,
                            ),
                        ],
                    ),
                    DetailComponent(
                        InitialApplicationQuestionsForms.OpeningQuestion.HELP_WITH_CHOOSING_A_LICENCE,
                        InitialApplicationQuestionsForms.OpeningQuestion.HELP_WITH_CHOOSING_A_LICENCE_CONTENT,
                    ),
                ],
                default_button_name=generic.CONTINUE,
                back_link=BackLink(
                    TradeControlLicenceQuestions.TradeControlLicenceQuestion.BACK,
                    reverse_lazy("apply_for_a_licence:start"),
                ),
            ),
            reference_name_form(),
            Form(
                title=TradeControlLicenceQuestions.ControlActivity.TITLE,
                description=TradeControlLicenceQuestions.ControlActivity.DESCRIPTION,
                questions=[
                    RadioButtons(
                        name="tc_activity",
                        options=[
                            Option("transfer_of_goods", "Transfer of goods"),
                            Option("provision_of_finance", "Finance or financial services"),
                            Option("provision_of_advertising", "General advertising or promotion services"),
                            Option("provision_of_insurance", "Insurance or reinsurance"),
                            Option("provision_of_transportation", "Transportation services"),
                            Option("maritime_anti_piracy", "Maritime anti-piracy"),
                            Option(
                                "tc_activity_other",
                                "Other",
                                components=[
                                    TextInput(
                                        title=TradeControlLicenceQuestions.ControlActivity.OTHER_DESCRIPTION,
                                        name="other",
                                        optional=False,
                                    )
                                ],
                            ),
                        ],
                    ),
                ],
                default_button_name=generic.CONTINUE,
            ),
            Form(
                title=TradeControlLicenceQuestions.ControlProduct.TITLE,
                description=TradeControlLicenceQuestions.ControlProduct.DESCRIPTION,
                questions=[
                    RadioButtons(
                        name="tc_product_category",
                        options=[
                            Option("category_a", "Category A"),
                            Option("category_b", "Category B"),
                            Option("category_c", "Category C"),
                        ],
                    ),
                ],
                default_button_name=generic.SAVE_AND_CONTINUE,
            ),
        ]
    )


def transhipment_questions():
    return FormGroup(
        [
            Form(
                title=TranshipmentQuestions.TranshipmentLicenceQuestion.TITLE,
                description=TranshipmentQuestions.TranshipmentLicenceQuestion.DESCRIPTION,
                questions=[
                    RadioButtons(
                        name="application_type",
                        options=[
                            Option(
                                key=CaseTypes.SITL,
                                value=TranshipmentQuestions.TranshipmentLicenceQuestion.STANDARD_LICENCE,
                                description=TranshipmentQuestions.TranshipmentLicenceQuestion.STANDARD_LICENCE_DESCRIPTION,
                            ),
                        ],
                    ),
                ],
                default_button_name=generic.CONTINUE,
                back_link=BackLink(
                    TranshipmentQuestions.TranshipmentLicenceQuestion.BACK, reverse_lazy("apply_for_a_licence:start")
                ),
            ),
            reference_name_form(),
            Form(
                title=ExportLicenceQuestions.ExportType.TITLE,
                description=ExportLicenceQuestions.ExportType.DESCRIPTION,
                questions=[
                    RadioButtons(
                        name="export_type",
                        options=[
                            Option("temporary", ExportLicenceQuestions.ExportType.TEMPORARY),
                            Option("permanent", ExportLicenceQuestions.ExportType.PERMANENT),
                        ],
                    ),
                ],
                default_button_name=generic.CONTINUE,
            ),
            goods_categories(),
            told_by_an_official_form(),
        ]
    )


def MOD_questions(application_type=None):
    return FormGroup(
        [
            Form(
                title=MODQuestions.WhatAreYouApplyingFor.TITLE,
                description=MODQuestions.WhatAreYouApplyingFor.DESCRIPTION,
                questions=[
                    RadioButtons(
                        name="application_type",
                        options=[
                            Option(
                                key=CaseTypes.F680,
                                value=MODQuestions.WhatAreYouApplyingFor.PERMISSION_TITLE,
                                description=MODQuestions.WhatAreYouApplyingFor.PERMISSION_DESCRIPTION,
                            ),
                            Option(
                                key=CaseTypes.EXHC,
                                value=MODQuestions.WhatAreYouApplyingFor.EXHIBITION_CLEARANCE_TITLE,
                                description=MODQuestions.WhatAreYouApplyingFor.EXHIBITION_CLEARANCE_DESCRIPTION,
                            ),
                            Option(
                                key=CaseTypes.GIFT,
                                value=MODQuestions.WhatAreYouApplyingFor.GIFTING_CLEARANCE_TITLE,
                                description=MODQuestions.WhatAreYouApplyingFor.GIFTING_CLEARANCE_DESCRIPTION,
                            ),
                        ],
                    ),
                ],
                default_button_name=generic.CONTINUE,
                back_link=BackLink(MODQuestions.WhatAreYouApplyingFor.BACK, reverse_lazy("apply_for_a_licence:start")),
            ),
            conditional(
                application_type == CaseTypes.F680,
                Form(
                    title=MODQuestions.ConfirmationStatement.TITLE,
                    questions=[
                        Label(paragraph) for paragraph in MODQuestions.ConfirmationStatement.DESCRIPTION.split("\n")
                    ],
                    default_button_name=generic.CONFIRM_AND_CONTINUE,
                ),
            ),
            reference_name_form(),
        ]
    )
