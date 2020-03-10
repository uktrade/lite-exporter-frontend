from lite_forms.components import Form, RadioButtons, FormGroup, Option, TextInput, TextArea
from lite_forms.helpers import conditional


def end_use_details_form(is_standard_application):
    return FormGroup(
        [
            is_military_end_use_controls_form(),
            is_informed_wmd_form(),
            is_suspected_wmd_form(),
            conditional(is_standard_application, is_eu_military_form()),
        ]
    )


def is_military_end_use_controls_form():
    return Form(
        title="Have you received a letter from ECJU...",
        questions=[
            RadioButtons(
                name="is_military_end_use_controls",
                short_title="Military end use controls",
                options=[
                    Option(
                        key="yes",
                        value="Yes",
                        components=[
                            TextInput(
                                title="",
                                description="This reference is on the ECJU letter",
                                name="military_end_use_controls_ref",
                                optional=False,
                            ),
                        ],
                    ),
                    Option(key="no", value="No"),
                ],
                classes=["govuk-radios--inline"],
            )
        ],
    )


def is_informed_wmd_form():
    return Form(
        title="Have you been informed by ECJU that the products may be intended for ...",
        questions=[
            RadioButtons(
                name="is_informed_wmd",
                short_title="Informed WMD",
                title="",
                options=[
                    Option(
                        key="yes",
                        value="Yes",
                        components=[
                            TextInput(
                                title="",
                                description="This reference is on the ECJU letter",
                                name="informed_wmd_ref",
                                optional=False,
                            ),
                        ],
                    ),
                    Option(key="no", value="No"),
                ],
                classes=["govuk-radios--inline"],
            )
        ],
    )


def is_suspected_wmd_form():
    return Form(
        title="Do you know or suspect that the products might be used...",
        questions=[
            RadioButtons(
                name="is_suspected_wmd",
                short_title="Suspected",
                title="",
                options=[
                    Option(
                        key="yes",
                        value="Yes",
                        components=[
                            TextArea(
                                name="suspected_wmd_ref",
                                title="",
                                description="Provide details",
                                extras={"max_length": 2200},
                                optional=False,
                            )
                        ],
                    ),
                    Option(key="no", value="No"),
                ],
                classes=["govuk-radios--inline"],
            )
        ],
    )


def is_eu_military_form():
    return Form(
        title="Have you received European military products...",
        questions=[
            RadioButtons(
                name="is_eu_military",
                short_title="EU Military",
                title="",
                options=[
                    Option(
                        key="yes",
                        value="Yes",
                        components=[
                            TextArea(
                                name="eu_military_ref",
                                title="",
                                description="Provide details",
                                extras={"max_length": 2200},
                                optional=False,
                            )
                        ],
                    ),
                    Option(key="no", value="No"),
                ],
                classes=["govuk-radios--inline"],
            )
        ],
    )
