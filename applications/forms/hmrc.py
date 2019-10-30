from lite_forms.components import Form, TextArea, Summary, Label, HiddenField

from applications.components import back_to_task_list, footer_label
from core.builtins.custom_tags import str_date


def confirm_organisation_form(organisation):
    return Form(title='Confirm that you want to make a query for this organisation',
                questions=[
                    Summary(values={
                        'Name': organisation['name'],
                        'Registration Number': organisation['registration_number'],
                        'EORI Number': organisation['eori_number'],
                        'VAT Number': organisation['vat_number'],
                        'Created at': str_date(organisation['created_at']),
                    }),
                    HiddenField('organisation', organisation['id'])
                ],
                default_button_name='Confirm and continue')


def query_explanation_form(application_id):
    return Form(title='Explain the reason behind your query',
                questions=[
                    TextArea(name='reasoning',
                             extras={
                                 'max_length': 280,
                             })
                ],
                default_button_name='Save and mark as done',
                back_link=back_to_task_list(application_id),
                footer_label=footer_label(application_id))
