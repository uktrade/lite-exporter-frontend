from core.builtins.custom_tags import str_date
from libraries.forms.components import Form, RadioButtons, Option


def select_your_organisation_form(organisations):
    return Form('Which organisation do you want to sign in to?',
                'You can change this later from the home screen.',
                [
                    RadioButtons(name='organisation',
                                 options=[
                                     Option(x['id'], x['name'], 'Member since ' + str_date(x['joined_at'])) for x in organisations
                                 ])
                ],
                default_button_name='Save and continue',
                back_link=None)
