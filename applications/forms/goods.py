from goods.helpers import good_summary
from lite_content.lite_exporter_frontend import strings
from lite_forms.components import Form, HiddenField, SideBySideSection, Select, QuantityInput, CurrencyInput, \
    RadioButtons, Option
from lite_forms.helpers import conditional


def good_on_application_form(good, units, title, prefix=""):
    return Form(
        title=title,
        questions=[
            conditional(good, good_summary(good)),
            conditional(good, HiddenField(name="good_id", value=good.get("id"))),
            CurrencyInput(title=strings.goods.CreateGoodOnApplicationForm.TITLE, name=prefix + "value"),
            SideBySideSection(
                questions=[
                    QuantityInput(title=strings.goods.CreateGoodOnApplicationForm.QUANTITY, name=prefix + "quantity"),
                    Select(title=strings.goods.CreateGoodOnApplicationForm.UNITS, name=prefix + "unit", options=units),
                ]
            ),
            RadioButtons(
                name='is_good_incorporated',
                title="Is the good incorporated?",
                description="Good incorporated description",
                options=[
                    Option(True, "Yes"),
                    Option(False, "No")
                ],
                classes=["govuk-radios--inline"],
            )
        ],
        javascript_imports=["/assets/javascripts/specific/add_good.js"],
    )
