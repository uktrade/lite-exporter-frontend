from lite_forms.components import RadioButtons, Form, Option, FormGroup

from applications.forms.end_user import third_parties_standard_form
from lite_content.lite_exporter_frontend.applications import ThirdPartyForm

option_list = {
    "agent": "Agent or broker",
    "additional_end_user": "Additional end user",
    "intermediate_consignee": "Intermediate consignee",
    "submitter": "Authorised submitter",
    "consultant": "Consultant",
    "contact": "Contact",
    "exporter": "Exporter",
}


def third_party_forms(application):
    if application["export_type"] and application["export_type"]["key"] == "permanent":
        form_options = option_list.copy()
        del form_options["additional_end_user"]
    else:
        form_options = option_list.copy()

    third_party_form = third_parties_standard_form(application, ThirdPartyForm.TITLE)
    options = [Option(key, value) for key, value in form_options.items()]
    options.append(Option("other", "Other", show_or=True))
    third_party_type = Form(
        title=ThirdPartyForm.TITLE,
        questions=[RadioButtons("sub_type", options=options)],
        default_button_name="Continue",
    )
    third_party_form[0] = third_party_type
    return FormGroup(third_party_form)
