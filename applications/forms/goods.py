from goods.helpers import good_summary
from lite_content.lite_exporter_frontend import strings
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


def good_on_application_form(good, units, title):
    return Form(
        title=title,
        questions=[
            conditional(good, good_summary(good)),
            conditional(good, HiddenField(name="good_id", value=good.get("id"))),
            CurrencyInput(title=strings.goods.CreateGoodOnApplicationForm.TITLE, name="value"),
            SideBySideSection(
                questions=[
                    QuantityInput(title=strings.goods.CreateGoodOnApplicationForm.QUANTITY, name="quantity"),
                    Select(title=strings.goods.CreateGoodOnApplicationForm.UNITS, name="unit", options=units),
                ]
            ),
            RadioButtons(
                name="is_good_incorporated",
                title=strings.goods.CreateGoodOnApplicationForm.INCORPORATED,
                description=strings.goods.CreateGoodOnApplicationForm.INCORPORATED_DESCRIPTION,
                options=[Option(True, strings.goods.CreateGoodOnApplicationForm.INCORPORATED_YES), Option(False, strings.goods.CreateGoodOnApplicationForm.INCORPORATED_NO)],
                classes=["govuk-radios--inline"],
            ),
        ],
        javascript_imports=["/assets/javascripts/add_good.js"],
    )
