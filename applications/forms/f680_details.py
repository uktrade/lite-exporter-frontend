from applications.components import back_to_task_list
from core.services import get_f680_clearance_types
from lite_content.lite_exporter_frontend.goods import F680Details

from lite_forms.components import Form, Filter, Checkboxes


def f680_details_form(application_id):
    return Form(
        title=F680Details.TITLE,
        description=F680Details.DESCRIPTION,
        questions=[
            Filter(),
            Checkboxes(
                name="f680_clearance_types",
                options=get_f680_clearance_types(application_id),
                classes=["govuk-checkboxes--small"],
                show_select_links=True,
            ),
        ],
        javascript_imports=["/assets/javascripts/filter-checkbox-list.js"],
        default_button_name=F680Details.BUTTON,
        back_link=back_to_task_list(application_id),
    )
