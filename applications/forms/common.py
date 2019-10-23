from django.urls import reverse_lazy
from lite_forms.components import HiddenField, Form, BackLink, TextArea, HTMLBlock, RadioButtons, Option, List, Label, \
    Group
from lite_forms.generators import confirm_form


def respond_to_query_form(application_id, ecju_query):
    return Form(title='Respond to query',
                description='',
                questions=[
                    HTMLBlock('<div class="app-ecju-query__text" style="display: block; max-width: 100%;">' +
                              ecju_query['question'] +
                              '</div><br><br>'),
                    TextArea(name='response',
                             title='Your response',
                             description='You won\'t be able to edit this once you\'ve submitted it.',
                             extras={
                                 'max_length': 2200,
                             }),
                    HiddenField(name='form_name', value='respond_to_query')
                ],
                back_link=BackLink('Back to application', reverse_lazy('applications:application-detail',
                                                                       kwargs={'pk': application_id,
                                                                               'type': 'ecju-queries'})),
                default_button_name='Submit response')


def ecju_query_respond_confirmation_form(edit_response_url):
    return confirm_form(title='Are you sure you want to send this response?',
                        confirmation_name='confirm_response',
                        hidden_field='ecju_query_response_confirmation',
                        yes_label='Yes, send the response',
                        no_label='No, change my response',
                        back_link_text='Back to edit response',
                        back_url=edit_response_url,
                        submit_button_text='Continue')


def edit_type_form(application_id):
    return Form(title='How do you want to change your application?',
                description='Depending on your answer it can take longer to reach a decision.',
                questions=[
                    RadioButtons(name='edit-type',
                                 options=[
                                     Option(key='minor',
                                            value='Change a site, or delete a good, third party or country',
                                            description='This won\'t impact the time it takes to reach a decision.'),
                                     Option(key='major',
                                            value='Something else',
                                            description='This will impact the time it takes to reach a decision.')
                                 ])],
                back_link=BackLink('Back to application', reverse_lazy('applications:application-detail',
                                                                       kwargs={'pk': application_id,
                                                                               'type': 'ecju-queries'})),
                default_button_name='Continue')
