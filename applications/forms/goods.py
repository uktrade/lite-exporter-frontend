from conf.constants import EXHIBITION
from core.services import get_units, get_item_types
from goods.helpers import good_summary
from lite_content.lite_exporter_frontend.goods import AddGoodToApplicationForm
from lite_forms.components import (
    Form,
    HiddenField,
    SideBySideSection,
    Select,
    QuantityInput,
    CurrencyInput,
    RadioButtons,
    Option,
    TextArea,
)


def good_on_application_form(request, good, sub_case_type):

    if sub_case_type["key"] != EXHIBITION:
        return Form(
            title=AddGoodToApplicationForm.TITLE,
            description=AddGoodToApplicationForm.DESCRIPTION,
            questions=[
                good_summary(good),
                HiddenField(name="good_id", value=good.get("id")),
                CurrencyInput(
                    title=AddGoodToApplicationForm.VALUE.TITLE,
                    description=AddGoodToApplicationForm.VALUE.DESCRIPTION,
                    name="value",
                ),
                SideBySideSection(
                    questions=[
                        QuantityInput(
                            title=AddGoodToApplicationForm.Quantity.TITLE,
                            description=AddGoodToApplicationForm.Quantity.DESCRIPTION,
                            name="quantity",
                        ),
                        Select(
                            title=AddGoodToApplicationForm.Units.TITLE,
                            description=AddGoodToApplicationForm.Units.DESCRIPTION,
                            name="unit",
                            options=get_units(request),
                        ),
                    ]
                ),
                RadioButtons(
                    name="is_good_incorporated",
                    title=AddGoodToApplicationForm.Incorporated.TITLE,
                    description=AddGoodToApplicationForm.Incorporated.DESCRIPTION,
                    options=[
                        Option(True, AddGoodToApplicationForm.Incorporated.YES),
                        Option(False, AddGoodToApplicationForm.Incorporated.NO),
                    ],
                    classes=["govuk-radios--inline"],
                ),
            ],
            javascript_imports=["/assets/javascripts/add_good.js"],
        )
    else:
        return Form(
            title="Select what will be exhibited for the product",
            description="",
            questions=[
                HiddenField(name="good_id", value=good.get("id")),
                RadioButtons(title="", description="", name="item_type", options=get_item_types(request)),
            ],
        )
