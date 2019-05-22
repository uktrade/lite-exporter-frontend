from libraries.forms.components import Form, Question, InputType, Section

new_end_user_form = Section('', '', [
    Form(title='Add an end user',
         description='Select all sites that apply.',
         questions=[
             Question('Company Name', '', InputType.INPUT, 'name'),
         ],
         default_button_name='Save and continue'),
    Form(title='Add an end user',
         description='Select all sites that apply.',
         questions=[
             Question('Government/commercial organisation/other', '', InputType.INPUT, 'name'),
         ],
         default_button_name='Save and continue'),
    Form(title='Add an end user',
         description='Select all sites that apply.',
         questions=[
             Question('Organisation URL', '', InputType.INPUT, 'name'),
         ],
         default_button_name='Save and continue'),
    Form(title='Add an end user',
         description='Select all sites that apply.',
         questions=[
             Question('Where\'s the company basd', '', InputType.TEXTAREA, ''),
             Question('Country?', '', InputType.INPUT, 'name'),
         ],
         default_button_name='Save and continue')
])
