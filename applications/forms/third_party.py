from lite_forms.components import RadioButtons, Form, Option, FormGroup

from lite_content.lite_exporter_frontend.applications import ThirdPartyForm
from applications.forms.end_user import _party_name_form, _party_website_form, _party_address_form

option_list = {
    "agent": ThirdPartyForm.Options.AGENT,
    "additional_end_user": ThirdPartyForm.Options.ADDITIONAL_END_USER,
    "intermediate_consignee": ThirdPartyForm.Options.INTERMEDIATE_CONSIGNEE,
    "submitter": ThirdPartyForm.Options.SUBMITTER,
    "consultant": ThirdPartyForm.Options.CONSULTANT,
    "contact": ThirdPartyForm.Options.CONTACT,
    "exporter": ThirdPartyForm.Options.EXPORTER,
}


def _third_party_type_form(title, options):
    return Form(title=title, questions=[RadioButtons("sub_type", options=options)], default_button_name="Continue",)


def third_party_forms(application):
    if application["export_type"] and application["export_type"]["key"] == "permanent":
        form_options = option_list.copy()
        del form_options["additional_end_user"]
    else:
        form_options = option_list.copy()
    options = [Option(key, value) for key, value in form_options.items()]
    options.append(Option("other", "Other", show_or=True))

    return FormGroup(
        [
            _third_party_type_form(ThirdPartyForm.TITLE, options),
            _party_name_form(),
            _party_website_form(),
            _party_address_form(),
        ]
    )
