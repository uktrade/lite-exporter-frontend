from lite_forms.components import RadioButtons, Form, Option, TextArea, Select, TextInput

from core.services import get_countries


def new_end_user_forms():
    return [
        Form(title='Who will be the final recipient (end-user) of your goods?',
             description='',
             questions=[
                 RadioButtons('type',
                              options=[
                                  Option('government', 'A Government Organisation'),
                                  Option('commercial', 'A Commercial Organisation'),
                                  Option('individual', 'An Individual'),
                                  Option('other', 'Other', show_or=True),
                              ]),
             ],
             pk='1',
             default_button_name='Continue'),
        Form(title='Enter the final recipient\'s name',
             description='',
             questions=[
                 TextInput('name'),
             ],
             default_button_name='Continue'),
        Form(title='Enter the final recipient\'s web address (URL)',
             description='',
             questions=[
                 TextInput('website', optional=True),
             ],
             default_button_name='Continue'),
        Form(title='Where\'s the final recipient based?',
             description='',
             questions=[
                 TextArea('address', 'Address'),
                 Select(title='Country',
                        name='country',
                        options=get_countries(None, True)),
             ],
             default_button_name='Save and continue')
    ]
