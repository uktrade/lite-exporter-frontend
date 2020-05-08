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
                options=[Option(key, value) for key, value in get_contract_types(request).items()],
                classes=["govuk-checkboxes--small"],
            ),
            TextInput(name="other_text", title="Other sector or contract type"),
        ],
        default_button_name=strings.SAVE,
        back_link=back_to_task_list(application_id),
    )
