from django.urls import reverse, reverse_lazy

from conf.settings import env
from core.builtins.custom_tags import get_string
from core.services import get_control_list_entries, get_pv_gradings
from goods.helpers import good_summary
from lite_content.lite_exporter_frontend import strings
from lite_forms.common import control_list_entry_question, pv_grading_question
from lite_forms.components import (
    Form,
    TextArea,
    RadioButtons,
    Option,
    BackLink,
    FileUpload,
    TextInput,
    HTMLBlock,
    HiddenField,
    Button,
    DateInput,
)
from lite_forms.generators import confirm_form
from lite_forms.styles import ButtonStyle


def add_goods_questions(allow_query=True, back_link=BackLink, prefix=""):
    if allow_query:
        description = strings.GOODS_CREATE_CONTROL_CODE_REQUIRED_DESC
        is_your_good_controlled_options = [
            Option(key="yes", value=strings.GOODS_CREATE_CONTROL_CODE_YES, show_pane="pane_" + prefix + "control_code"),
            Option(key="no", value=strings.GOODS_CREATE_CONTROL_CODE_NO),
            Option(key="unsure", value=strings.GOODS_CREATE_CONTROL_CODE_UNSURE),
        ]
    else:
        description = strings.APPLICATION_GOODS_CONTROL_CODE_REQUIRED_DESCRIPTION
        is_your_good_controlled_options = [
            Option(key="yes", value=strings.GOODS_CREATE_CONTROL_CODE_YES, show_pane="pane_" + prefix + "control_code"),
            Option(key="no", value=strings.GOODS_CREATE_CONTROL_CODE_NO),
        ]

    # fmt: off
    pv_grading_panes = f"pane_{prefix}pv_grading," \
                       f"pane_{prefix}pv_grading_custom," \
                       f"pane_{prefix}pv_grading_prefix," \
                       f"pane_{prefix}pv_grading_suffix," \
                       f"pane_{prefix}pv_grading_issuing_authority," \
                       f"pane_{prefix}pv_grading_reference," \
                       f"pane_{prefix}pv_grading_date_of_issue," \
                       f"pane_{prefix}pv_grading_comment"
    # fmt: on

    form = Form(
        title=strings.GOODS_CREATE_TITLE,
        questions=[
            TextArea(title="Description", description="", name=prefix + "description", extras={"max_length": 280,},),
            RadioButtons(
                title="Is the product controlled?",
                description=description,
                name=prefix + "is_good_controlled",
                options=is_your_good_controlled_options,
                classes=["govuk-radios--inline"],
            ),
            control_list_entry_question(
                control_list_entries=get_control_list_entries(None, convert_to_options=True),
                title="Control list classification",
                description="<noscript>If your product is controlled, enter its "
                "control list classification. </noscript>For example, ML1a.",
                name=prefix + "control_code",
                inset_text=False,
            ),
            RadioButtons(
                title="Does the product hold a PV grading?",
                name=prefix + "holds_pv_grading",
                options=[
                    Option(key="yes", value="Yes", show_pane=pv_grading_panes),
                    Option(key="no", value="No"),
                    Option(key="grading_required", value="I need to have it issued")
                ],
                classes=["govuk-radios--inline"],
            ),
            pv_grading_question(
                pv_gradings=get_pv_gradings(request=None, convert_to_options=True),
                title="What is your product's PV grading?",
                description="If your product is graded, enter its grading. For example, 'UK classified' or 'other'.",
                name=prefix + "pv_grading",
                inset_text=False,
            ),
            TextInput(title="Custom grading if the above is 'other'", name=prefix + "pv_grading_custom"),
            TextInput(title="Prefix", name=prefix + "pv_grading_prefix", optional=True),
            TextInput(title="Suffix", name=prefix + "pv_grading_suffix", optional=True),
            TextInput(title="Issuing authority", name=prefix + "pv_grading_issuing_authority"),
            TextInput(title="Reference", name=prefix + "pv_grading_reference"),
            DateInput(title="Date of issue", prefix=prefix, name=prefix + "pv_grading_date_of_issue"),
            TextArea(
                title="Comment",
                description="",
                name=prefix + "pv_grading_comment",
                extras={"max_length": 280,},
                optional=True,
            ),
            RadioButtons(
                title="Will the product be incorporated into another product?",
                description="",
                name=prefix + "is_good_end_product",
                options=[Option(key="yes", value="Yes"), Option(key="no", value="No")],
                classes=["govuk-radios--inline"],
            ),
            TextInput(title="Part number (optional)", name=prefix + "part_number", optional=True),
        ],
        back_link=back_link,
    )

    return form


def are_you_sure(good_id):
    return Form(
        title=get_string("clc.clc_form.title"),
        description=get_string("clc.clc_form.description"),
        questions=[
            TextInput(
                title="What do you think is your product's control list entry?",
                description="For example, ML1a.",
                optional=True,
                name="not_sure_details_control_code",
            ),
            TextArea(
                title="Further details about your product",
                description="Please enter details of why you don't know if your product is controlled",
                optional=True,
                name="not_sure_details_details",
            ),
        ],
        back_link=BackLink("Back to product", reverse("goods:good", kwargs={"pk": good_id})),
    )


def pv_query(good_id):
    return Form(
        title="Create a PV grading query",
        description="By saving you are creating a PV query that cannot be altered",
        questions = [
            TextArea(
                title="Additional information about your product",
                description="Please enter details of why you need a PV grading",
                optional=True,
                name="pv_grading_additional_information",
            ),
        ],
    )

def edit_form(good_id):
    return Form(
        title="Edit product",
        questions=[
            TextArea(title="Description", description="", name="description", extras={"max_length": 280,},),
            RadioButtons(
                title="Is the product controlled?",
                description='If you don\'t know you can use <a class="govuk-link" href="'
                + env("PERMISSIONS_FINDER_URL")
                + '">Permissions Finder</a>.',
                name="is_good_controlled",
                options=[
                    Option(key="yes", value="Yes", show_pane="pane_control_code"),
                    Option(key="no", value="No"),
                    Option(key="unsure", value="I don't know"),
                ],
                classes=["govuk-radios--inline"],
            ),
            control_list_entry_question(
                control_list_entries=get_control_list_entries(None, convert_to_options=True),
                title="Control list classification",
                description="<noscript>If your product is controlled, enter its control list classification. </noscript>For example, ML1a.",
                name="control_code",
                inset_text=False,
            ),
            RadioButtons(
                title="Will the product be incorporated into another product?",
                description="",
                name="is_good_end_product",
                options=[Option(key=True, value="Yes"), Option(key=False, value="No")],
                classes=["govuk-radios--inline"],
            ),
            TextInput(title="Part number (optional)", name="part_number", optional=True),
        ],
        buttons=[
            Button("Save", "submit", ButtonStyle.DEFAULT),
            Button(
                value="Delete product",
                action="",
                style=ButtonStyle.WARNING,
                link=reverse_lazy("goods:delete", kwargs={"pk": good_id}),
                float_right=True,
            ),
        ],
    )


def attach_documents_form(back_url, description):
    return Form(
        get_string("goods.documents.attach_documents.title"),
        description,
        [
            FileUpload("documents"),
            TextArea(
                title=get_string("goods.documents.attach_documents.description_field_title"),
                optional=True,
                name="description",
                extras={"max_length": 280},
            ),
        ],
        buttons=[Button("Save", "submit", disable_double_click=True)],
        back_link=BackLink(get_string("goods.documents.attach_documents.back_to_good"), back_url),
    )


def respond_to_query_form(good_id, ecju_query):
    return Form(
        title="Respond to query",
        description="",
        questions=[
            HTMLBlock(
                '<div class="app-ecju-query__text" style="display: block; max-width: 100%;">'
                + ecju_query["question"]
                + "</div><br><br>"
            ),
            TextArea(
                name="response",
                title="Your response",
                description="You won't be able to edit this once you've submitted it.",
                extras={"max_length": 2200},
            ),
            HiddenField(name="form_name", value="respond_to_query"),
        ],
        back_link=BackLink(
            "Back to product", reverse_lazy("goods:good_detail", kwargs={"pk": good_id, "type": "ecju-queries"})
        ),
        default_button_name="Submit response",
    )


def ecju_query_respond_confirmation_form(edit_response_url):
    return confirm_form(
        title="Are you sure you want to send this response?",
        confirmation_name="confirm_response",
        hidden_field="ecju_query_response_confirmation",
        yes_label="Yes, send the response",
        no_label="No, change my response",
        back_link_text="Back to edit response",
        back_url=edit_response_url,
    )


def delete_good_form(good):
    return Form(
        title="Are you sure you want to delete this product?",
        questions=[good_summary(good)],
        buttons=[
            Button(value="Yes, delete the product", action="submit", style=ButtonStyle.WARNING),
            Button(
                value="Cancel",
                action="",
                style=ButtonStyle.SECONDARY,
                link=reverse_lazy("goods:edit", kwargs={"pk": good["id"]}),
            ),
        ],
    )
