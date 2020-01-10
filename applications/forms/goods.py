from goods.helpers import good_summary
from lite_content.lite_exporter_frontend.goods import AddPreexistingGoodToApplicationForm
from lite_forms.components import (
    Form,
    HiddenField,
    SideBySideSection,
    Select,
    QuantityInput,
    CurrencyInput,
    RadioButtons,
    Option,
)
from lite_forms.helpers import conditional


def good_on_application_form(good, units):
    return Form(
        title=AddPreexistingGoodToApplicationForm.TITLE,
        description=AddPreexistingGoodToApplicationForm.DESCRIPTION,
        questions=[
            conditional(good, good_summary(good)),
            conditional(good, HiddenField(name="good_id", value=good.get("id"))),
            CurrencyInput(
                title=AddPreexistingGoodToApplicationForm.VALUE.TITLE,
                description=AddPreexistingGoodToApplicationForm.VALUE.DESCRIPTION,
                name="value",
            ),
            SideBySideSection(
                questions=[
                    QuantityInput(
                        title=AddPreexistingGoodToApplicationForm.Quantity.TITLE,
                        description=AddPreexistingGoodToApplicationForm.Quantity.DESCRIPTION,
                        name="quantity",
                    ),
                    Select(
                        title=AddPreexistingGoodToApplicationForm.Units.TITLE,
                        description=AddPreexistingGoodToApplicationForm.Units.DESCRIPTION,
                        name="unit",
                        options=units,
                    ),
                ]
            ),
            RadioButtons(
                name="is_good_incorporated",
                title=AddPreexistingGoodToApplicationForm.Incorporated.TITLE,
                description=AddPreexistingGoodToApplicationForm.Incorporated.DESCRIPTION,
                options=[
                    Option(True, AddPreexistingGoodToApplicationForm.Incorporated.YES),
                    Option(False, AddPreexistingGoodToApplicationForm.Incorporated.NO),
                ],
                classes=["govuk-radios--inline"],
            ),
        ],
        javascript_imports=["/assets/javascripts/add_good.js"],
    )
