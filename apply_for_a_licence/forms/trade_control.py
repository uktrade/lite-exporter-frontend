from django.urls import reverse_lazy

from conf.constants import CaseTypes
from lite_content.lite_exporter_frontend import generic
from lite_content.lite_exporter_frontend.applications import (
    InitialApplicationQuestionsForms,
    TradeControlLicenceQuestions,
)
from lite_forms.components import (
    Form,
    RadioButtons,
    Option,
    BackLink,
    DetailComponent,
    TextArea,
)


def application_type_form():
    return Form(
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
            TradeControlLicenceQuestions.TradeControlLicenceQuestion.BACK, reverse_lazy("apply_for_a_licence:start")
        ),
    )


def activity_form():
    return Form(
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
                        "other",
                        "Other",
                        components=[
                            TextArea(
                                title=TradeControlLicenceQuestions.ControlActivity.OTHER_DESCRIPTION,
                                name="tc_activity_other",
                                optional=False,
                                rows=1,
                                extras={"max_length": 100},
                            )
                        ],
                    ),
                ],
            ),
        ],
        default_button_name=generic.CONTINUE,
    )


def product_category_form():
    return Form(
        title=TradeControlLicenceQuestions.ControlProduct.TITLE,
        description=TradeControlLicenceQuestions.ControlProduct.DESCRIPTION,
        questions=[
            RadioButtons(
                name="tc_product_category",
                options=[
                    Option("category_a", "Category A", TradeControlLicenceQuestions.ControlProduct.CATEGORY_A_HINT),
                    Option("category_b", "Category B", TradeControlLicenceQuestions.ControlProduct.CATEGORY_B_HINT),
                    Option("category_c", "Category C", TradeControlLicenceQuestions.ControlProduct.CATEGORY_C_HINT),
                ],
            ),
        ],
        default_button_name=generic.SAVE_AND_CONTINUE,
    )
