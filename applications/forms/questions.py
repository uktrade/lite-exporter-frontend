from lite_forms.components import FormGroup, Form, RadioButtons, Option, TextArea, FileUpload, DateInput, CurrencyInput
from lite_content.lite_exporter_frontend.applications import F680Questions
from lite_content.lite_exporter_frontend import generic


def questions_forms():
    return FormGroup(
        [
            Form(
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
                                        description=F680Questions.Expedited.DESCRIPTION,
                                    )
                                ],
                            ),
                            Option(key=False, value="No"),
                        ],
                    )
                ],
                default_button_name=generic.SAVE_AND_CONTINUE,
            ),
            Form(
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
                                        name="foreign_technology_description",
                                        description=F680Questions.ForeignTechnology.DESCRIPTION,
                                    )
                                ],
                            ),
                            Option(key=False, value="No"),
                        ],
                    )
                ],
                default_button_name=generic.SAVE_AND_CONTINUE,
            ),
            Form(
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
                                        name="locally_manufactured_description",
                                        description=F680Questions.LocallyManufactured.DESCRIPTION
                                    )
                                ],
                            ),
                            Option(key=False, value="No"),
                        ],
                    )
                ],
                default_button_name=generic.SAVE_AND_CONTINUE,
            ),
            Form(
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
            ),
            Form(
                title=F680Questions.EWRequirement.TITLE,
                questions=[
                    RadioButtons(
                        name="electronic_warfare_requirement",
                        options=[
                            Option(
                                key=True,
                                value="Yes",
                                components=[
                                    FileUpload(
                                        name="electronic_warfare_requirement_attachment",
                                        description=F680Questions.EWRequirement.ATTACHMENT,
                                    )
                                ],
                            ),
                            Option(key=False, value="No"),
                        ],
                    )
                ],
                default_button_name=generic.SAVE_AND_CONTINUE,
            ),
            Form(
                title=F680Questions.UKServiceEquipment.TITLE,
                questions=[
                    RadioButtons(
                        name="uk_service_equipment",
                        options=[
                            Option(
                                key=True,
                                value="Yes",
                                components=[
                                    TextArea(
                                        name="uk_service_equipment_description",
                                        description=F680Questions.UKServiceEquipment.DESCRIPTION
                                    ),
                                ],
                            ),
                            Option(key=False, value="No"),
                        ],
                    )
                ],
                default_button_name=generic.SAVE_AND_CONTINUE,
            ),
            Form(
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
                ]
            ),
            Form(
                title=F680Questions.ProspectValue.TITLE,
                questions=[
                    CurrencyInput(name="value")
                ],
                default_button_name=generic.SAVE_AND_CONTINUE,
            ),
        ],
        show_progress_indicators=True
    )
