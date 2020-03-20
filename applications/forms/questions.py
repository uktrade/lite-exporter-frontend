from lite_content.lite_exporter_frontend import generic
from lite_content.lite_exporter_frontend.applications import F680Questions
from lite_forms.components import FormGroup, Form, RadioButtons, Option, TextArea, DateInput, CurrencyInput


def questions_forms():
    return FormGroup(
        [
            expedited_form(),
            foreign_technology_form(),
            locally_manufactured_form(),
            mtcr_form(),
            electronic_warfare_form(),
            uk_service_equipment_form(),
            uk_service_equipment_type_form(),
            prospect_value_form(),
        ],
        show_progress_indicators=True,
    )


def expedited_form():
    return Form(
        title=F680Questions.Expedited.TITLE,
        questions=[
            RadioButtons(
                name="expedited",
                options=[
                    Option(
                        key=True,
                        value="Yes",
                        components=[
                            DateInput(title=F680Questions.Expedited.DATE, name="expedited_date", prefix=""),
                            TextArea(
                                name="expedited_description",
                                title="",
                                description=F680Questions.PROVIDE_DETAILS,
                                extras={"max_length": 2200},
                                optional=False,
                            ),
                        ],
                    ),
                    Option(key=False, value="No"),
                ],
            )
        ],
        default_button_name=generic.SAVE_AND_CONTINUE,
    )


def foreign_technology_form():
    return Form(
        title=F680Questions.ForeignTechnology.TITLE,
        questions=[
            RadioButtons(
                name="foreign_technology",
                options=[
                    Option(
                        key=True,
                        value="Yes",
                        components=[
                            TextArea(
                                title=F680Questions.PROVIDE_DETAILS,
                                name="foreign_technology_description",
                                description=F680Questions.ForeignTechnology.DESCRIPTION,
                                extras={"max_length": 2200},
                                optional=False,
                            ),
                        ],
                    ),
                    Option(key=False, value="No"),
                ],
            )
        ],
        default_button_name=generic.SAVE_AND_CONTINUE,
    )


def locally_manufactured_form():
    return Form(
        title=F680Questions.LocallyManufactured.TITLE,
        questions=[
            RadioButtons(
                name="locally_manufactured",
                options=[
                    Option(
                        key=True,
                        value="Yes",
                        components=[
                            TextArea(
                                title=F680Questions.PROVIDE_DETAILS,
                                name="locally_manufactured_description",
                                extras={"max_length": 2200},
                                optional=False,
                            ),
                        ],
                    ),
                    Option(key=False, value="No"),
                ],
            )
        ],
        default_button_name=generic.SAVE_AND_CONTINUE,
    )


def mtcr_form():
    return Form(
        title=F680Questions.MtcrType.TITLE,
        questions=[
            RadioButtons(
                name="mtcr_type",
                options=[
                    Option(key="mtcr_category_1", value="Yes, Category 1"),
                    Option(key="mtcr_category_2", value="Yes, Category 2"),
                    Option(key="none", value="No"),
                    Option(key="unknown", value="I don't know", show_or=True),
                ],
            )
        ],
        default_button_name=generic.SAVE_AND_CONTINUE,
    )


def electronic_warfare_form():
    return Form(
        title=F680Questions.EWRequirement.TITLE,
        questions=[
            RadioButtons(
                name="electronic_warfare_requirement",
                options=[
                    Option(key=True, description=F680Questions.EWRequirement.ATTACHMENT, value="Yes",),
                    Option(key=False, value="No"),
                ],
            )
        ],
        default_button_name=generic.SAVE_AND_CONTINUE,
    )


def uk_service_equipment_form():
    return Form(
        title=F680Questions.UKServiceEquipment.TITLE,
        questions=[
            RadioButtons(
                name="uk_service_equipment",
                options=[
                    Option(
                        key=True,
                        value="Yes",
                        components=[TextArea(name="uk_service_equipment_description", extras={"max_length": 2200},),],
                    ),
                    Option(key=False, value="No"),
                ],
            )
        ],
        default_button_name=generic.SAVE_AND_CONTINUE,
    )


def uk_service_equipment_type_form():
    return Form(
        title=F680Questions.UKServiceEquipment.TYPE,
        questions=[
            RadioButtons(
                name="uk_service_equipment_type",
                options=[
                    Option(key="mod_funded", value="MOD funded"),
                    Option(key="part_mod_part_venture", value="Part MOD funded / part private venture"),
                    Option(key="private_venture", value="Private venture"),
                ],
            ),
        ],
    )


def prospect_value_form():
    return Form(
        title=F680Questions.ProspectValue.TITLE,
        questions=[CurrencyInput(name="value")],
        default_button_name=generic.SAVE_AND_CONTINUE,
    )
