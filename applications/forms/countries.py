from applications.components import back_to_task_list
from core.services import get_countries, get_contract_types
from lite_content.lite_exporter_frontend import strings
from lite_forms.components import Form, Filter, Checkboxes, RadioButtons, Option, TextInput, HiddenField


def countries_form(application_id):
    return Form(
        title=strings.applications.DestinationForm.TITLE,
        description=strings.applications.DestinationForm.DESCRIPTION,
        questions=[
            Filter(),
            Checkboxes(
                name="countries[]",
                options=get_countries(None, True),
                classes=["govuk-checkboxes--small"],
                show_select_links=True,
            ),
        ],
        javascript_imports=["/assets/javascripts/filter-checkbox-list.js"],
        default_button_name=strings.SAVE,
        back_link=back_to_task_list(application_id),
    )


def contract_type_form(application_id):
    return Form(
        title="Do you want the same sectors and contract types applied to each country?",
        description="Description here",
        questions=[
            RadioButtons(
                "choice",
                [Option("all", "Yes"), Option("individual", "No, each country needs a different combination"),],
            )
        ],
        default_button_name=strings.SAVE,
        back_link=back_to_task_list(application_id),
    )


def contract_type_per_country_form(request, application_id, current_country, country_name):
    return Form(
        title="Select the sectors and contract types for " + country_name,
        description=strings.applications.DestinationForm.DESCRIPTION,
        questions=[
            HiddenField("country", current_country),
            Checkboxes(
                name="contracts[]",
                options=[
                    Option(key="nuclear_related", value="Nuclear related",),
                    Option(key="navy", value="Navy",),
                    Option(key="army", value="Army",),
                    Option(key="air_force", value="Air force",),
                    Option(key="police", value="Police",),
                    Option(key="ministry_of_interior", value="Ministry of Interior",),
                    Option(key="other_security_forces", value="Other security forces",),
                    Option(key="Companies_nuclear_related", value="Companies nuclear related",),
                    Option(key="Maritime_anti_piracy", value="Maritime anti-piracy",),
                    Option(key="Aircraft_manufacturers", value="Aircraft manufacturers",),
                    Option(key="registered_firearm_dealers", value="Registered firearm dealers",),
                    Option(key="oil_and_gas_industry", value="Oil and gas industry",),
                    Option(key="pharmaceutical_or_medical", value="Pharmaceutical or medical",),
                    Option(key="media", value="Media",),
                    Option(key="private_military", value="Private military",),
                    Option(key="education", value="Education",),
                    Option(key="for_the_exporters_own_use", value="For the exporters own use",),
                ],
                classes=["govuk-checkboxes--small"],
            ),
            TextInput(name="other_text", title="Other sector or contract type"),
        ],
        default_button_name=strings.SAVE,
        back_link=back_to_task_list(application_id),
    )
