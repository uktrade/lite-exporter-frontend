from core.services import get_countries
from libraries.forms.components import Form, ArrayQuestion, InputType, Option, Question

which_location_form = Form(title='Are your goods located at your organisation or an external location?',
                           description='',
                           questions=[
                               ArrayQuestion('', '', InputType.RADIOBUTTONS, 'organisation_or_external', [
                                   Option('organisation', 'My Organisation'),
                                   Option('external', 'External location'),
                               ])
                           ],
                           default_button_name='Continue')

new_location_form = Form(title='Add a new external location',
                         description='',
                         questions=[
                             Question('Company name', '', InputType.INPUT, 'name'),
                             Question('Address', '', InputType.TEXTAREA, 'address'),
                             ArrayQuestion(title='Country',
                                           description='',
                                           input_type=InputType.AUTOCOMPLETE,
                                           name='country',
                                           data=get_countries(None, True)),
                         ],
                         default_button_name='Save and continue')
