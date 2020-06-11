from lite_content.lite_exporter_frontend.compliance import OpenReturnsForm
from lite_forms.components import FormGroup, Form, Select, Option, FileUpload
from datetime import datetime


START_YEAR = 2020


def get_years():
    current_year = datetime.now().year
    previous_year = current_year - 1
    return [
        Option(key=current_year, value=current_year),
        Option(key=previous_year, value=previous_year)
    ]


def annual_return_form_group():
    return FormGroup(
        [
            Form(
                title=OpenReturnsForm.Year.TITLE,
                description=OpenReturnsForm.Year.DESCRIPTION,
                questions=[
                    Select(title=OpenReturnsForm.Year.FIELD_TITLE, description=OpenReturnsForm.Year.FiELD_DESCRIPTION, name="year", options=get_years())
                ],
                default_button_name="Continue",
            ),
            Form(title="Upload", description="blah", questions=[FileUpload()], default_button_name="Submit",),
        ]
    )
