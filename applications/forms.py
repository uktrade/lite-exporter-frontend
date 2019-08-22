from django.urls import reverse_lazy

from libraries.forms.components import Form, BackLink, TextArea, HTMLBlock


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
                                 'max_length': 5000,
                             })
                ],
                back_link=BackLink('Back to application', reverse_lazy('applications:application-detail',
                                                                       kwargs={'pk': application_id,
                                                                               'type': 'ecju-queries'})),
                default_button_name='Submit response')
