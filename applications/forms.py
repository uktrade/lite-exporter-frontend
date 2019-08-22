from libraries.forms.components import Form, BackLink, TextArea


def respond_to_query_form():
    return Form(title='Respond to query',
                description='Query goes here',
                questions=[
                    TextArea(name='response',
                             title='Your response',
                             description='You won\'t be able to edit this once you\'ve submitted it.',
                             extras={
                                 'max_length': 280,
                             })
                ],
                back_link=BackLink('Back to application', ''))
