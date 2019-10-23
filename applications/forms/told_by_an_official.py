from lite_forms.components import Form, RadioButtons, Option, TextInput


def told_by_an_official_form():
    return Form(title='Have you been told that you need an export licence by an official?',
                description='This could be a letter or email from HMRC or another government department.',
                questions=[
                    RadioButtons(name='have_you_been_informed',
                                 options=[
                                     Option('yes', 'Yes',
                                            show_pane='pane_reference_number_on_information_form'),
                                     Option('no', 'No')
                                 ],
                                 classes=['govuk-radios--inline']),
                    TextInput(title='What was the reference number if you were provided one?',
                              description='This is the reference found on the letter or '
                                          'email to tell you to apply for an export licence.',
                              name='reference_number_on_information_form',
                              optional=True),
                ],
                default_button_name='Save and continue')
