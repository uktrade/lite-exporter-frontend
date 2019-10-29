from lite_forms.components import Form, TextArea

from applications.components import back_to_task_list, footer_label


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
