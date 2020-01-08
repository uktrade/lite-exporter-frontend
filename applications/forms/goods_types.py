from conf.constants import HMRC_QUERY
from lite_content.lite_exporter_frontend import strings
from core.services import get_control_list_entries
from lite_content.lite_exporter_frontend.goods import PERMISSION_FINDER_LINK
from lite_forms.common import control_list_entry_question
from lite_forms.components import TextArea, RadioButtons, Option, Form
from lite_forms.helpers import conditional


def goods_type_form(application_type: str = None):
    return Form(
        title=strings.GoodTypes.Overview.TITLE,
        questions=[
            TextArea(title="Description", name="description", extras={"max_length": 2000,}),
            RadioButtons(
                title="Are your products controlled?",
                description="Products that aren't on the "
                + PERMISSION_FINDER_LINK
                + " may be affected by military end use controls, current trade sanctions and embargoes or weapons of "
                "mass destruction controls. If your products aren't subject to any controls, you'll get a no licence "
                "required (NLR) document from ECJU.",
                name="is_good_controlled",
                options=[Option(key="yes", value="Yes", show_pane="pane_control_code"), Option(key="no", value="No")],
                classes=["govuk-radios--inline"],
            ),
            control_list_entry_question(
                control_list_entries=get_control_list_entries(None, convert_to_options=True),
                name="control_code",
                inset_text=False,
            ),
            conditional(
                application_type != HMRC_QUERY,
                RadioButtons(
                    title="Will the products be incorporated into other products",
                    name="is_good_end_product",
                    options=[Option(key="yes", value="Yes"), Option(key="no", value="No")],
                    classes=["govuk-radios--inline"],
                ),
            ),
        ],
    )
