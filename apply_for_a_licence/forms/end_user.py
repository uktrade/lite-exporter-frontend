from core.builtins.custom_tags import get_string
from core.services import get_countries
from libraries.forms.components import Form, Question, InputType, Section, ArrayQuestion, Option, RadioButtons, \
    FileUpload, BackLink, TextArea
from libraries.forms.generators import confirm_form


def new_end_user_form():
    return Section('', '', [
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
                 Question('', '', InputType.INPUT, 'name'),
             ],
             pk='2',
             default_button_name='Continue'),
        Form(title='Enter the final recipient\'s web address (URL)',
             description='',
             questions=[
                 Question('', '', InputType.INPUT, 'website', optional=True),
             ],
             pk='3',
             default_button_name='Continue'),
        Form(title='Where\'s the final recipient based?',
             description='',
             questions=[
                 TextArea('address', 'Address'),
                 ArrayQuestion(title='Country',
                               description='',
                               input_type=InputType.AUTOCOMPLETE,
                               name='country',
                               data=get_countries(None, True)),
             ],
             pk='4',
             default_button_name='Save and continue')
    ])


def attach_document_form(draft_url):
    return Form(get_string('end_user.documents.attach_documents.title'),
                get_string('end_user.documents.attach_documents.description'),
                [
                    FileUpload('documents'),
                    TextArea(title=get_string('end_user.documents.attach_documents.description_field_title'),
                             description=get_string('end_user.documents.attach_documents.description_field_details'),
                             name='description',
                             extras={
                                 'max_length': 280,
                             })
                ],
                back_link=BackLink(get_string('end_user.documents.attach_documents.back_to_application_overview'), draft_url))


def delete_document_confirmation_form(overview_url):
    return confirm_form(title='Are you sure you want to delete this document?',
                        confirmation_name='delete_document_confirmation',
                        back_link_text=get_string('end_user.documents.attach_documents.back_to_application_overview'),
                        back_url=overview_url
                        )
