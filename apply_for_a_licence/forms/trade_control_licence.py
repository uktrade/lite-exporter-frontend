from django.urls import reverse_lazy

from conf.constants import CaseTypes
from core.services import get_trade_control_activities, get_trade_control_product_categories
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


def activity_form(request):
    activities = get_trade_control_activities(request)
    options = []

    for activity in activities:
        option = Option(activity["key"], activity["value"])

        if activity["key"] == "other":
            option.components = [
                TextArea(
                    title=TradeControlLicenceQuestions.ControlActivity.OTHER_DESCRIPTION,
                    name="tc_activity_other",
                    optional=False,
                    rows=1,
                    extras={"max_length": 100},
                )
            ]

        options.append(option)

    return Form(
        title=TradeControlLicenceQuestions.ControlActivity.TITLE,
        description=TradeControlLicenceQuestions.ControlActivity.DESCRIPTION,
        questions=[RadioButtons(name="tc_activity", options=options)],
        default_button_name=generic.CONTINUE,
    )


def product_category_form(request):
    product_categories = get_trade_control_product_categories(request)
    options = [Option(product_category["key"], product_category["value"]) for product_category in product_categories]

    return Form(
        title=TradeControlLicenceQuestions.ControlProduct.TITLE,
        description=TradeControlLicenceQuestions.ControlProduct.DESCRIPTION,
        questions=[RadioButtons(name="tc_product_category", options=options)],
        default_button_name=generic.SAVE_AND_CONTINUE,
    )
