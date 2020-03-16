from lite_forms.components import FormGroup, Form, RadioButtons, Option, TextArea, FileUpload


def questions_forms():
    return FormGroup(
        [
            Form(
                title="Does your application need to be expedited?",
                questions=[
                    RadioButtons(
                        name="expedited",
                        options=[
                            Option(
                                key=True,
                                value="Yes",
                                components=[TextArea(name="expedited_description", description="Description 1")],
                            ),
                            Option(key=False, value="No"),
                        ],
                    )
                ],
            ),
            Form(
                title="Is any foreign technology or information is involved in the proposed release",
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
                                        description="include written release agreements or clearances from the originating nations",
                                    )
                                ],
                            ),
                            Option(key=False, value="No"),
                        ],
                    )
                ],
            ),
            Form(
                title="Is local assembly/local manufacture of the product is required",
                questions=[
                    RadioButtons(
                        name="locally_manufactured",
                        options=[
                            Option(
                                key=True,
                                value="Yes",
                                components=[
                                    TextArea(
                                        name="locally_manufactured_description", description="Additional information"
                                    )
                                ],
                            ),
                            Option(key=False, value="No"),
                        ],
                    )
                ],
            ),
            Form(
                title="Are the goods rated under the Missile Technology Control Regime (MTCR)",
                questions=[
                    RadioButtons(
                        name="mtcr_type",
                        options=[
                            # Option(key=True, value="Yes", components=[
                            #     RadioButtons(
                            #         title="What category are the goods under?",
                            #         name="question_4",
                            #         options=[
                            #             Option(key="mtcr_category_1", value="MTCR category 1"),
                            #             Option(key="mtcr_category_2", value="MTCR category 2"),
                            #         ]
                            #     )
                            # ]),
                            Option(key="mtcr_category_1", value="Yes, Category 1"),
                            Option(key="mtcr_category_2", value="Yes, Category 2"),
                            Option(key="none", value="No"),
                            Option(key="unknown", value="I don't know", show_or=True),
                        ],
                    )
                ],
            ),
            Form(
                title="Is there is a requirement to release UK MOD owned electronic warfare (EW) data or information in support of this export",
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
                                        description="Please attach part A of the EW data release capture form",
                                    )
                                ],
                            ),
                            Option(key=False, value="No"),
                        ],
                    )
                ],
            ),
            Form(
                title="Is the equipment or a version of it due to enter service with the UK armed forces",
                questions=[
                    RadioButtons(
                        name="uk_service_equipment",
                        options=[
                            Option(
                                key=True,
                                value="Yes",
                                components=[
                                    TextArea(name="uk_service_equipment_description", description="Please elabortate"),
                                    RadioButtons(
                                        title="Please select whether the equipment is:",
                                        name="uk_service_equipment_type",
                                        options=[
                                            Option(key=True, value="MOD funded"),
                                            Option(key=False, value="Part MOD funded / part private venture"),
                                            Option(key=False, value="Private venture"),
                                        ],
                                    ),
                                ],
                            ),
                            Option(key=False, value="No"),
                        ],
                    )
                ],
            ),
            Form(
                title="What is the total value of the application prospect",
                questions=[TextArea(name="question_7", description="Total value:")],
            ),
        ]
    )
