from lite_forms.components import FormGroup, Form, Select, Option, FileUpload
from datetime import datetime


START_YEAR = 2020


def get_years():
    current_year = datetime.now().year
    return [Option(key=year, value=year) for year in range(current_year, START_YEAR - 1, -1)]


def annual_return_form_group():
    return FormGroup(
        [
            Form(
                title="Select year",
                description="blah",
                questions=[
                    Select(title="", description="", name="year", options=get_years(), include_default_select=False,)
                ],
                default_button_name="Continue",
            ),
            Form(title="Upload", description="blah", questions=[FileUpload()], default_button_name="Submit",),
        ]
    )
