from lite_forms.common import country_question
from lite_forms.components import RadioButtons, Form, Option, TextArea, TextInput, FormGroup, HiddenField

from core.services import get_countries


class QuestionBlocks:
    q_name = TextInput(title='What\'s the end user\'s name?',
                       name='end_user.name')
    q_individual = [
        TextInput(title='What\'s the end user\'s email address?',
                  name='contact_email'),
        TextInput(title='What\'s the end user\'s telephone number?',
                  name='contact_telephone')
    ]
    q_nature_of_business = TextInput(title='What\'s the nature of the end user\'s business?',
                                     name='nature_of_business')
    q_primary_contact_details = [
        TextInput(title='What\'s the primary contact\'s name?',
                  name='contact_email'),
        TextInput(title='What\'s the primary contact\'s email address?',
                  name='contact_email'),
        TextInput(title='What\'s the primary contact\'s telephone number?',
                  name='contact_telephone')
    ]
    q_address = [
        TextArea(title='What\'s the end user\'s address?',
                 description='This is usually the delivery address or registered office for the person '
                             'receiving the goods',
                 name='end_user.address'),
        country_question(countries=get_countries(None, True),
                         prefix='end_user.'),
    ]
    q_hidden_validate_only = HiddenField('validate_only', True)


def apply_for_an_end_user_advisory_form(individual, commercial):
    form_group = FormGroup([
        Form(title='Check if someone is eligible to import your goods',
             questions=[
                 RadioButtons(title='How would you describe this end user?',
                              name='end_user.sub_type',
                              options=[
                                  Option('government', 'A Government Organisation'),
                                  Option('commercial', 'A Commercial Organisation'),
                                  Option('individual', 'An Individual'),
                                  Option('other', 'Other', show_or=True),
                              ]),
             ],
             default_button_name='Continue'),
    ])

    form = Form(title='Tell us more about this recipient',
                questions=[],
                default_button_name='Continue')
    form.questions.append(QuestionBlocks.q_name)
    if individual:
        [form.questions.append(question) for question in QuestionBlocks.q_individual]
    elif commercial:
        form.questions.append(QuestionBlocks.q_nature_of_business)
        [form.questions.append(question) for question in QuestionBlocks.q_primary_contact_details]
    else:
        [form.questions.append(question) for question in QuestionBlocks.q_primary_contact_details]
    [form.questions.append(question) for question in QuestionBlocks.q_address]
    form.questions.append(QuestionBlocks.q_hidden_validate_only)

    form_group.forms.append(form)

    form_group.forms.append(
        Form(title='More information about this advisory',
             questions=[
                 TextArea(title='What\'s your reasoning behind this query?',
                          optional=True,
                          name='reasoning',
                          extras={
                              'max_length': 2000,
                          }),
                 TextArea(title='Is there any other information you can provide about this user?',
                          description='This can help to speed up the query and give you a more accurate result',
                          optional=True,
                          name='notes',
                          extras={
                              'max_length': 2000,
                          }),
                 HiddenField('validate_only', False),
             ],
             default_button_name='Submit'))
    return form_group
