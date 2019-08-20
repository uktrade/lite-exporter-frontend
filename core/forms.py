from libraries.forms.components import Form, RadioButtons, Option


def select_your_organisation_form(organisations):
    return Form('Which organisation do you want to sign in to?',
                'You can change this later from the home screen.',
                [
                    RadioButtons(name='description',
                                 options=[
                                     Option('key', 'BAE Systems', 'Member since 5 August 2019'),
                                     Option('key', 'BAE Systems 2', 'Member since 6 August 2019'),
                                     Option('key', 'BAE Systems 3', 'Member since 7 August 2019')
                                 ])
                ],
                default_button_name='Save and continue',
                back_link=None)
