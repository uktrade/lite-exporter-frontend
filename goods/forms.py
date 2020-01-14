from django.urls import reverse, reverse_lazy

from core.services import get_control_list_entries
from goods.helpers import good_summary
from goods.services import get_document_missing_reasons
from lite_content.lite_exporter_frontend import generic
from lite_content.lite_exporter_frontend.goods import (
    CreateGoodForm,
    CLCQueryForm,
    EditGoodForm,
    DocumentSensitivityForm,
    AttachDocumentForm,
    RespondToQueryForm,
    GoodsList,
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
    Breadcrumbs,
    FormGroup,
)
from lite_forms.generators import confirm_form
from lite_forms.helpers import conditional
from lite_forms.styles import ButtonStyle


def add_goods_questions(application_pk=None):
    return Form(
        title=conditional(application_pk, CreateGoodForm.TITLE, "Add a product to your organisation"),
        questions=[
            TextArea(
                title=CreateGoodForm.Description.TITLE,
                description=CreateGoodForm.Description.DESCRIPTION,
                name="description",
                extras={"max_length": 280},
            ),
            RadioButtons(
                title=CreateGoodForm.IsControlled.TITLE,
                description=conditional(
                    application_pk, CreateGoodForm.IsControlled.DESCRIPTION, CreateGoodForm.IsControlled.CLC_REQUIRED,
                ),
                name="is_good_controlled",
                options=[
                    Option(key="yes", value=CreateGoodForm.IsControlled.YES, show_pane="pane_control_code"),
                    Option(key="no", value=CreateGoodForm.IsControlled.NO),
                    conditional(not application_pk, Option(key="unsure", value=CreateGoodForm.IsControlled.UNSURE)),
                ],
                classes=["govuk-radios--inline"],
            ),
            control_list_entry_question(
                control_list_entries=get_control_list_entries(None, convert_to_options=True),
                title=CreateGoodForm.ControlListEntry.TITLE,
                description=CreateGoodForm.ControlListEntry.DESCRIPTION,
                name="control_code",
                inset_text=False,
            ),
            RadioButtons(
                title="Does the product hold a PV grading?",
                name="holds_pv_grading",
                options=[
                    Option(key="yes", value="Yes"),
                    Option(key="no", value="No"),
                    Option(key="grading_required", value="I need to have it issued"),
                ],
                classes=["govuk-radios--inline"],
            ),
            TextInput(title=CreateGoodForm.PartNumber.TITLE, name="part_number", optional=True),
        ],
        back_link=conditional(
            application_pk,
            BackLink(generic.BACK, reverse_lazy("applications:goods", kwargs={"pk": application_pk})),
            Breadcrumbs(
                [
                    BackLink(generic.SERVICE_NAME, reverse_lazy("core:hub")),
                    BackLink(GoodsList.TITLE, reverse_lazy("goods:goods")),
                    BackLink(GoodsList.CREATE_GOOD),
                ]
            ),
        ),
        default_button_name=CreateGoodForm.BUTTON,
    )


def pv_details_form():
    return Form(
        title="Create a query for this product",
        description="By saving you are creating a query that cannot be altered",
        questions=[
            pv_grading_question(
                pv_gradings=get_pv_gradings(request=None, convert_to_options=True),
                title="What is your product's PV grading?",
                description="If your product is graded, enter its grading. For example, 'UK classified' or 'other'.",
                name="pv_grading",
                inset_text=False,
            ),
            TextInput(title="Custom grading if the above is 'other'", name="pv_grading_custom"),
            TextInput(title="Prefix", name="pv_grading_prefix", optional=True),
            TextInput(title="Suffix", name="pv_grading_suffix", optional=True),
            TextInput(title="Issuing authority", name="pv_grading_issuing_authority"),
            TextInput(title="Reference", name="pv_grading_reference"),
            DateInput(title="Date of issue", prefix="pv_grading_date_of_issue"),
            TextArea(
                title="Comment", description="", name="pv_grading_comment", extras={"max_length": 280,}, optional=True,
            ),
        ],
        default_button_name="Save",
    )


def add_good_form_group(holds_pv_grading: str = None):
    return FormGroup([add_goods_questions(), conditional(holds_pv_grading == "yes", pv_details_form())])


def raise_a_pv_or_clc_query(good_id, raise_a_clc: bool, raise_a_pv: bool):
    questions = []

    if raise_a_clc:
        questions += [
            TextInput(
                title=CLCQueryForm.CLCCode.TITLE,
                description=CLCQueryForm.CLCCode.DESCRIPTION,
                name="not_sure_details_control_code",
                optional=True,
            ),
            TextArea(title=CLCQueryForm.Additional.DESCRIPTION, name="not_sure_details_details", optional=True,),
        ]

    if raise_a_pv:
        questions += [
            TextArea(
                title="Please enter details of why you need a PV grading",
                name="pv_grading_additional_information",
                optional=True,
            ),
        ]

    return Form(
        title="Create a query for this product",
        description="By saving you are creating a query that cannot be altered",
        questions=questions,
        back_link=BackLink("Back to product", reverse("goods:good", kwargs={"pk": good_id})),
        default_button_name="Save",
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


def document_grading_form(request, good_id):
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
        back_link=BackLink("Back", reverse_lazy("goods:good", kwargs={"pk": good_id})),
        default_button_name=DocumentSensitivityForm.BUTTON,
    )


def attach_documents_form(back_link):
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
        back_link=back_link,
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
                extras={"max_length": 2200},
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


def raise_query_confirmation_form(overview_url):
    return confirm_form(
        title="do you wish to raise a query?",
        description="Would you like to raise a query at this current time? "
        "If a query is raised you will not be able to edit the good",
        confirmation_name="confirm_raise_query",
        back_link_text="back",
        back_url=overview_url,
    )
