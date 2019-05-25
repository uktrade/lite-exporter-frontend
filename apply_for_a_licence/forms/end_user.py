from libraries.forms.components import Form, Question, InputType, Section, ArrayQuestion, Option

new_end_user_form = Section('', '', [
    Form(title='Who will be the final recipient (end-user) of your goods?',
         description='',
         questions=[
             ArrayQuestion('',
                           '',
                           InputType.RADIOBUTTONS,
                           'type',
                           data=[
                               Option('government', 'A Government Organisation'),
                               Option('commercial', 'A Commercial Organisation'),
                               Option('other', 'Other', show_or=True),
                           ]),
         ],
         default_button_name='Continue'),
    Form(title='Enter the final recipient\'s organisation or company name',
         description='',
         questions=[
             Question('', '', InputType.INPUT, 'name'),
         ],
         default_button_name='Continue'),
    Form(title='Enter an organisation or company web link (URL)',
         description='',
         questions=[
             Question('', '', InputType.INPUT, 'website', optional=True),
         ],
         default_button_name='Continue'),
    Form(title='Where\'s the company based?',
         description='',
         questions=[
             Question('Address', '', InputType.TEXTAREA, 'address'),
             Question('Country', '', InputType.INPUT, 'country'),
         ],
         default_button_name='Save and continue')
])
