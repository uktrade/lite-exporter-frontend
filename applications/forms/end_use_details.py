from lite_content.lite_exporter_frontend.applications import EndUseDetailsForm
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
        title=EndUseDetailsForm.INFORMED_TO_APPLY,
        questions=[
            RadioButtons(
                name="is_military_end_use_controls",
                short_title=EndUseDetailsForm.EndUseDetailsSummaryList.INFORMED_TO_APPLY,
                options=[
                    Option(
                        key="yes",
                        value="Yes",
                        components=[
                            TextInput(
                                title="",
                                description=EndUseDetailsForm.REFERENCE_ECJU_LETTER,
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
        title=EndUseDetailsForm.INFORMED_WMD,
        questions=[
            RadioButtons(
                name="is_informed_wmd",
                short_title=EndUseDetailsForm.EndUseDetailsSummaryList.INFORMED_WMD,
                title="",
                options=[
                    Option(
                        key="yes",
                        value="Yes",
                        components=[
                            TextInput(
                                title="",
                                description=EndUseDetailsForm.REFERENCE_ECJU_LETTER,
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
        title=EndUseDetailsForm.SUSPECTED_WMD,
        questions=[
            RadioButtons(
                name="is_suspected_wmd",
                short_title=EndUseDetailsForm.EndUseDetailsSummaryList.SUSPECTED_WMD,
                title="",
                options=[
                    Option(
                        key="yes",
                        value="Yes",
                        components=[
                            TextArea(
                                name="suspected_wmd_ref",
                                title="",
                                description=EndUseDetailsForm.PROVIDE_DETAILS,
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
        title=EndUseDetailsForm.EU_MILITARY,
        questions=[
            RadioButtons(
                name="is_eu_military",
                short_title=EndUseDetailsForm.EndUseDetailsSummaryList.EU_MILITARY,
                title="",
                options=[
                    Option(
                        key="yes",
                        value="Yes",
                        components=[
                            RadioButtons(
                                name="is_compliant_limitations_eu",
                                title=EndUseDetailsForm.IS_COMPLIANT_LIMITATIONS_EU,
                                short_title=EndUseDetailsForm.EndUseDetailsSummaryList.IS_COMPLIANT_LIMITATIONS_EU,
                                options=[
                                    Option(key="yes", value="Yes"),
                                    Option(
                                        key="no",
                                        value="No",
                                        components=[
                                            TextArea(
                                                name="compliant_limitations_eu_ref",
                                                title="",
                                                description=EndUseDetailsForm.PROVIDE_DETAILS,
                                                extras={"max_length": 2200},
                                                optional=False,
                                            )
                                        ],
                                    ),
                                ],
                            )
                        ],
                    ),
                    Option(key="no", value="No"),
                ],
                classes=["govuk-radios--inline"],
            )
        ],
    )
