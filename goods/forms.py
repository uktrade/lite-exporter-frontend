from django.urls import reverse, reverse_lazy
from lite_content.lite_exporter_frontend.goods import (
    CreateGoodForm,
    CLCQueryForm,
    EditGoodForm,
    DocumentSensitivityForm,
    AttachDocumentForm,
    RespondToQueryForm,
)

from core.services import get_control_list_entries
from core.services import get_pv_gradings
from goods.helpers import good_summary
from goods.services import get_document_missing_reasons
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
    Label,
    Select,
    Group,
)
from lite_forms.generators import confirm_form
from lite_forms.styles import ButtonStyle


def add_goods_questions(allow_query=True, back_link=BackLink, prefix=""):
    if allow_query:
        description = CreateGoodForm.IsControlled.DESCRIPTION
        is_your_good_controlled_options = [
            Option(key="yes", value=CreateGoodForm.IsControlled.YES, show_pane="pane_" + prefix + "control_code"),
            Option(key="no", value=CreateGoodForm.IsControlled.NO),
            Option(key="unsure", value=CreateGoodForm.IsControlled.UNSURE),
        ]
    else:
        description = CreateGoodForm.IsControlled.CLC_REQUIRED
        is_your_good_controlled_options = [
            Option(key="yes", value=CreateGoodForm.IsControlled.YES, show_pane="pane_" + prefix + "control_code"),
            Option(key="no", value=CreateGoodForm.IsControlled.NO),
        ]

    # Turns off black formatting for these lines because it breaks things
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
        title=CreateGoodForm.TITLE,
        questions=[
            TextArea(
                title=CreateGoodForm.Description.TITLE,
                description=CreateGoodForm.Description.DESCRIPTION,
                name=prefix + "description",
                extras={"max_length": 280,},
            ),
            RadioButtons(
                title=CreateGoodForm.IsControlled.TITLE,
                description=description,
                name=prefix + "is_good_controlled",
                options=is_your_good_controlled_options,
                classes=["govuk-radios--inline"],
            ),
            control_list_entry_question(
                control_list_entries=get_control_list_entries(None, convert_to_options=True),
                title=CreateGoodForm.ControlListEntry.TITLE,
                description=CreateGoodForm.ControlListEntry.DESCRIPTION,
                name=prefix + "control_code",
                inset_text=False,
            ),
            RadioButtons(
                title="Does the product hold a PV grading?",
                name=prefix + "holds_pv_grading",
                options=[
                    Option(key="yes", value="Yes", show_pane=pv_grading_panes),
                    Option(key="no", value="No"),
                    Option(key="grading_required", value="I need to have it issued"),
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
                title=CreateGoodForm.Incorporated.TITLE,
                description=CreateGoodForm.Incorporated.DESCRIPTION,
                name=prefix + "is_good_end_product",
                options=[
                    Option(key="no", value=CreateGoodForm.Incorporated.YES),
                    Option(key="yes", value=CreateGoodForm.Incorporated.NO),
                ],
                classes=["govuk-radios--inline"],
            ),
            TextInput(title=CreateGoodForm.PartNumber.TITLE, name=prefix + "part_number", optional=True),
        ],
        back_link=back_link,
        default_button_name=CreateGoodForm.BUTTON,
    )

    return form


def raise_a_clc_query(good_id):
    return Form(
        title=CLCQueryForm.TITLE,
        description=CLCQueryForm.DESCRIPTION,
        questions=[
            TextInput(
                title=CLCQueryForm.CLCCode.TITLE,
                description=CLCQueryForm.CLCCode.DESCRIPTION,
                optional=True,
                name="not_sure_details_control_code",
            ),
            TextArea(
                title=CLCQueryForm.Additional.TITLE,
                description=CLCQueryForm.Additional.DESCRIPTION,
                optional=True,
                name="not_sure_details_details",
            ),
        ],
        back_link=BackLink(CLCQueryForm.BACK_LINK, reverse("goods:good", kwargs={"pk": good_id})),
        default_button_name=CLCQueryForm.BUTTON,
    )


def pv_query(good_id):
    return Form(
        title="Create a PV grading query",
        description="By saving you are creating a PV query that cannot be altered",
        questions=[
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
        title=EditGoodForm.TITLE,
        description=EditGoodForm.DESCRIPTION,
        questions=[
            TextArea(
                title=EditGoodForm.Description.TITLE,
                description=EditGoodForm.Description.DESCRIPTION,
                name="description",
                extras={"max_length": 280,},
            ),
            RadioButtons(
                title=EditGoodForm.IsControlled.TITLE,
                description=EditGoodForm.IsControlled.DESCRIPTION,
                name="is_good_controlled",
                options=[
                    Option(key="yes", value=EditGoodForm.IsControlled.YES, show_pane="pane_control_code"),
                    Option(key="no", value=EditGoodForm.IsControlled.NO),
                    Option(key="unsure", value=EditGoodForm.IsControlled.UNSURE),
                ],
                classes=["govuk-radios--inline"],
            ),
            control_list_entry_question(
                control_list_entries=get_control_list_entries(None, convert_to_options=True),
                title=EditGoodForm.ControlListEntry.TITLE,
                description=EditGoodForm.IsControlled.DESCRIPTION,
                name="control_code",
                inset_text=False,
            ),
            RadioButtons(
                title=EditGoodForm.Incorporated.TITLE,
                description=EditGoodForm.Incorporated.DESCRIPTION,
                name="is_good_end_product",
                options=[
                    Option(key=True, value=EditGoodForm.Incorporated.YES),
                    Option(key=False, value=EditGoodForm.Incorporated.NO),
                ],
                classes=["govuk-radios--inline"],
            ),
            TextInput(title=EditGoodForm.PartNumber.TITLE, name="part_number", optional=True),
        ],
        buttons=[
            Button(EditGoodForm.Buttons.SAVE, "submit", ButtonStyle.DEFAULT),
            Button(
                value=EditGoodForm.Buttons.DELETE,
                action="",
                style=ButtonStyle.WARNING,
                link=reverse_lazy("goods:delete", kwargs={"pk": good_id}),
                float_right=True,
            ),
        ],
    )


def document_grading_form(request):
    select_options = get_document_missing_reasons(request)[0]["reasons"]

    return Form(
        title=DocumentSensitivityForm.TITLE,
        description=DocumentSensitivityForm.DESCRIPTION,
        questions=[
            RadioButtons(
                name="has_document_to_upload",
                options=[
                    Option(key="yes", value=DocumentSensitivityForm.Options.YES),
                    Option(key="no", value=DocumentSensitivityForm.Options.NO, show_pane="pane_ecju_contact"),
                ],
            ),
            Group(
                components=[
                    Label(text=DocumentSensitivityForm.ECJU_HELPLINE),
                    Select(name="missing_document_reason", options=select_options),
                ],
                name="ecju_contact",
                classes=["govuk-inset-text", "hidden"],
            ),
        ],
        default_button_name=DocumentSensitivityForm.BUTTON,
    )


def attach_documents_form(back_url):
    return Form(
        title=AttachDocumentForm.TITLE,
        description=AttachDocumentForm.DESCRIPTION,
        questions=[
            FileUpload("documents"),
            TextArea(
                title=AttachDocumentForm.Description.TITLE,
                optional=True,
                name="description",
                extras={"max_length": 280},
            ),
        ],
        buttons=[Button(AttachDocumentForm.BUTTON, "submit", disable_double_click=True)],
        back_link=BackLink(AttachDocumentForm.BACK_LINK, back_url),
    )


def respond_to_query_form(good_id, ecju_query):
    return Form(
        title=RespondToQueryForm.TITLE,
        description="",
        questions=[
            HTMLBlock(
                '<div class="app-ecju-query__text" style="display: block; max-width: 100%;">'
                + ecju_query["question"]
                + "</div><br><br>"
            ),
            TextArea(
                name="response",
                title=RespondToQueryForm.Response.TITLE,
                description=RespondToQueryForm.Response.DESCRIPTION,
                extras={"max_length": 2200,},
            ),
            HiddenField(name="form_name", value="respond_to_query"),
        ],
        back_link=BackLink(
            RespondToQueryForm.BACK_LINK,
            reverse_lazy("goods:good_detail", kwargs={"pk": good_id, "type": "ecju-queries"}),
        ),
        default_button_name=RespondToQueryForm.BUTTON,
    )


def ecju_query_respond_confirmation_form(edit_response_url):
    return confirm_form(
        title=RespondToQueryForm.ConfirmationForm.TITLE,
        confirmation_name="confirm_response",
        hidden_field="ecju_query_response_confirmation",
        yes_label=RespondToQueryForm.ConfirmationForm.YES,
        no_label=RespondToQueryForm.ConfirmationForm.NO,
        back_link_text=RespondToQueryForm.ConfirmationForm.BACK_LINK,
        back_url=edit_response_url,
    )


def delete_good_form(good):
    return Form(
        title=EditGoodForm.DeleteConfirmationForm.TITLE,
        questions=[good_summary(good)],
        buttons=[
            Button(value=EditGoodForm.DeleteConfirmationForm.YES, action="submit", style=ButtonStyle.WARNING),
            Button(
                value=EditGoodForm.DeleteConfirmationForm.NO,
                action="",
                style=ButtonStyle.SECONDARY,
                link=reverse_lazy("goods:edit", kwargs={"pk": good["id"]}),
            ),
        ],
    )
