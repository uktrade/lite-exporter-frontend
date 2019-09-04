from lite_forms.common import country_question
from lite_forms.components import RadioButtons, Form, Option, TextArea, TextInput, FormGroup, HiddenField

from core.services import get_countries


def apply_for_an_end_user_advisory_form():
    return FormGroup([
        Form(title='Check if someone is eligible to import your goods',
             questions=[
                 RadioButtons(title='How would you describe this end user?',
                              name='end_user.type',
                              options=[
                                  Option('government', 'A Government Organisation'),
                                  Option('commercial', 'A Commercial Organisation'),
                                  Option('individual', 'An Individual'),
                                  Option('other', 'Other', show_or=True),
                              ]),
             ],
             default_button_name='Continue'),
        Form(title='Tell us more about this recipient',
             questions=[
                 TextInput(title='What\'s the end user\'s name?',
                           name='end_user.name'),
                 TextInput(title='Enter the end user\'s web address?',
                           name='end_user.website',
                           optional=True),
                 TextArea(title='What\'s the end user\'s address?',
                          name='end_user.address'),
                 country_question(countries=get_countries(None, True),
                                  prefix='end_user.'),
                 HiddenField('validate_only', True),
             ],
             default_button_name='Continue'),
        Form(title='More information about this advisory',
             questions=[
                 TextArea(title='What\'s your reasoning behind this query?',
                          optional=True,
                          name='reasoning'),
                 TextArea(title='Any notes on this end user?',
                          optional=True,
                          name='notes'),
                 HiddenField('validate_only', False),
             ],
             default_button_name='Submit'),
    ], show_progress_indicators=True)
