from lite_content.lite_exporter_frontend import generic
from lite_forms.components import FormGroup, TextArea, Form, RadioButtons, Option, DateInput


def temporary_export_details_form():
    return FormGroup(
        [
            provide_export_details_form("Temporary export details"),
            is_temp_direct_control_form("Temporary export details"),
            proposed_product_return_date_form("Temporary export details"),
        ]
    )


def provide_export_details_form(caption):
    return Form(
        caption=caption,
        title="Provide details of why the export is temporary",
        questions=[
            TextArea(
                name="temp_export_details",
                short_title="Temporary export details",
                extras={"max_length": 2200},
                optional=False,
            )
        ],
        default_button_name=generic.SAVE_AND_CONTINUE,
    )


def is_temp_direct_control_form(caption):
    return Form(
        caption=caption,
        title="Will the products remain under your direct control whilst overseas",
        questions=[
            RadioButtons(
                name="is_temp_direct_control",
                short_title="Products remaining under your direct control",
                options=[
                    Option(key=True, value="Yes"),
                    Option(
                        key=False,
                        value="No",
                        components=[
                            TextArea(
                                name="temp_direct_control_details",
                                title="Provide details of who will be in control of the products while overseas and their relationship to you",
                                description="",
                                extras={"max_length": 2200},
                                optional=False,
                            )
                        ],
                    ),
                ],
                classes=["govuk-radios--inline"],
            )
        ],
        default_button_name=generic.SAVE_AND_CONTINUE,
    )


def proposed_product_return_date_form(caption):
    return Form(
        caption=caption,
        title="Proposed date the products will return to the UK",
        questions=[
            DateInput(
                title="",
                short_title="Date products returning to the UK",
                description="For example, 12 11 2020",
                name="proposed_return_date",
                prefix="",
                optional=False,
            ),
        ],
        default_button_name=generic.SAVE_AND_CONTINUE,
    )
