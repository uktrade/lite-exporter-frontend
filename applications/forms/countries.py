from applications.components import back_to_task_list
from core.services import get_countries
from lite_content.lite_exporter_frontend import strings
from lite_content.lite_exporter_frontend.applications import ContractTypes as contractTypeStrings
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
        default_button_name=strings.SAVE_AND_CONTINUE,
        back_link=back_to_task_list(application_id),
    )


def choose_contract_type_form():
    return Form(
        title=contractTypeStrings.ChooseContractTypeForm.TITLE,
        description=contractTypeStrings.ChooseContractTypeForm.DESCRIPTION,
        questions=[
            RadioButtons(
                "choice",
                [
                    Option("all", contractTypeStrings.ChooseContractTypeForm.ALL_COUNTRIES_OPTION),
                    Option("individual", contractTypeStrings.ChooseContractTypeForm.EACH_COUNTRY_INDIVIDUALLY_OPTION),
                ],
            )
        ],
        default_button_name=strings.SAVE,
        back_link=None,
    )


def contract_type_per_country_form(current_country, country_name):
    return Form(
        title=contractTypeStrings.AddContractTypesForm.TITLE + country_name,
        description=contractTypeStrings.AddContractTypesForm.DESCRIPTION,
        questions=[
            HiddenField("countries", current_country),
            Checkboxes(
                name="contract_types[]",
                options=[
                    Option(key="nuclear_related", value=contractTypeStrings.NUCLEAR_RELATED,),
                    Option(key="navy", value=contractTypeStrings.NAVY,),
                    Option(key="army", value=contractTypeStrings.ARMY,),
                    Option(key="air_force", value=contractTypeStrings.AIR_FORCE,),
                    Option(key="police", value=contractTypeStrings.POLICE,),
                    Option(key="ministry_of_interior", value=contractTypeStrings.MINISTRY_OF_INTERIOR,),
                    Option(key="other_security_forces", value=contractTypeStrings.OTHER_SECURITY_FORCES,),
                    Option(key="companies_nuclear_related", value=contractTypeStrings.COMPANIES_NUCLEAR_RELATED,),
                    Option(key="maritime_anti_piracy", value=contractTypeStrings.MARITIME_ANTI_PIRACY,),
                    Option(key="aircraft_manufacturers", value=contractTypeStrings.AIRCRAFT_MANUFACTURERS,),
                    Option(key="registered_firearm_dealers", value=contractTypeStrings.REGISTERED_FIREARM_DEALERS,),
                    Option(key="oil_and_gas_industry", value=contractTypeStrings.OIL_AND_GAS_INDUSTRY,),
                    Option(key="pharmaceutical_or_medical", value=contractTypeStrings.PHARMACEUTICAL_OR_MEDICAL,),
                    Option(key="media", value=contractTypeStrings.MEDIA,),
                    Option(key="private_military", value=contractTypeStrings.PRIVATE_MILITARY,),
                    Option(key="education", value=contractTypeStrings.EDUCATION,),
                    Option(key="for_the_exporters_own_use", value=contractTypeStrings.FOR_THE_EXPORTERS_OWN_USE,),
                    Option(key="other_contract_type", value=contractTypeStrings.OTHER,),
                ],
                classes=["govuk-checkboxes--small"],
            ),
            TextInput(name="other_contract_type_text", title=contractTypeStrings.AddContractTypesForm.PROVIDE_DETAILS),
        ],
        javascript_imports=["/assets/javascripts/filter-checkbox-list.js"],
        default_button_name=strings.SAVE_AND_CONTINUE,
    )
