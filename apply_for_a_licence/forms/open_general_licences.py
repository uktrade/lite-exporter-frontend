from core.services import get_control_list_entries, get_countries, get_open_general_licences, get_open_general_licence
from lite_content.lite_exporter_frontend import generic
from lite_forms.components import FormGroup, Form, AutocompleteInput, RadioButtons, Option, Custom, Heading, \
    Select
from lite_forms.styles import HeadingStyle


def open_general_licence_forms(request):
    control_list_entries = get_control_list_entries(request, True)
    countries = get_countries(request, True)
    selected_entry = request.POST.get("control_list_entry")
    selected_country = next((country.value for country in countries if country.key == request.POST.get("country")), "")
    open_general_licences = get_open_general_licences(request,
                                                      convert_to_options=True,
                                                      control_list_entry=request.POST.get("control_list_entry"),
                                                      country=request.POST.get("country"))
    selected_open_general_licence = get_open_general_licence(request, request.POST.get("open_general_licence"))

    return FormGroup(
        [
            Form(
                title="Enter the control list entries which apply to the product",
                questions=[
                    Select(name="control_list_entry", options=control_list_entries)
                ],
                default_button_name=generic.CONTINUE,
            ),
            Form(
                title="Enter the product's final destination",
                description="",
                questions=[AutocompleteInput(name="country", options=countries)],
                default_button_name=generic.CONTINUE,
            ),
            Form(
                title="Available open general licences",
                description=f"These are the open general licences described by **{selected_entry}** being exported to **{selected_country}**.",
                questions=[
                    RadioButtons(
                        name="open_general_licence",
                        description="Select the option which best matches your product and requirements.",
                        options=[*open_general_licences, Option(None, "None of the above", show_or=True)],
                    )
                ],
                default_button_name=generic.CONTINUE,
            ),
            Form(
                caption="Applying for",
                title=selected_open_general_licence["case_type"]["reference"]["value"] + " (" + selected_open_general_licence["name"] + ")",
                description=f"These are the open general licences described by **{selected_entry}** being exported to **{selected_country}**.",
                questions=[Heading("Before you continue", HeadingStyle.S),
                           Custom("components/ogl-step-list.html"),
                           Custom("components/ogl-warning.html")],
                default_button_name=generic.CONTINUE,
            ),
        ]
    )
