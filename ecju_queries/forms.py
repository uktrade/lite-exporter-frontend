from lite_forms.components import Form, HTMLBlock, TextArea, HiddenField, BackLink
from lite_forms.generators import confirm_form


def respond_to_query_form(back_link, ecju_query):
    return Form(
        title="Respond to query",
        questions=[
            HTMLBlock(
                '<div class="app-ecju-query__text" style="display: block; max-width: 100%;">'
                + ecju_query["question"]
                + "</div><br><br>"
            ),
            TextArea(name="response", title="Your response", description="", extras={"max_length": 2200,},),
            HiddenField(name="form_name", value="respond_to_query"),
        ],
        back_link=BackLink("Back", back_link,),
        default_button_name="Submit",
    )


def ecju_query_respond_confirmation_form(edit_response_url):
    return confirm_form(
        title="Confirm you want to send this response",
        confirmation_name="confirm_response",
        hidden_field="ecju_query_response_confirmation",
        yes_label="Confirm and send the response",
        no_label="Cancel",
        back_link_text="Back to edit response",
        back_url=edit_response_url,
        submit_button_text="Continue",
    )
