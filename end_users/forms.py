from django.urls import reverse_lazy
from lite_forms.common import country_question
from lite_forms.components import RadioButtons, Form, Option, TextArea, TextInput, FormGroup, HiddenField, HTMLBlock
from lite_forms.generators import success_page
from lite_forms.helpers import conditional

from core.builtins.custom_tags import reference_code
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
    return FormGroup([
        Form(title='Confirm how your goods will be used',
             questions=[
                 HTMLBlock(
                     '<ul class="govuk-list govuk-list--bullet">'
                     '<li class="govuk-!-margin-bottom-5">I have checked the <a class="govuk-link" href="https://scsanctions.un.org/fop/fop?xml=htdocs/resources/xml/en/consolidated.xml&xslt=htdocs/resources/xsl/en/consolidated.xsl">UN Security Council Committee’s list</a> and my goods will not be used by anyone named on this list</li>' # noqa
                     '<li class="govuk-!-margin-bottom-5">I have checked the <a class="govuk-link" href="https://permissions-finder.service.trade.gov.uk/">Department for International Trade’s list of controlled goods</a> and my goods are not controlled</li>' # noqa
                     '<li class="govuk-!-margin-bottom-5">I have not been previously informed by the Export Control Joint Unit that my goods could be used to make chemical, biological or nuclear weapons</li>' # noqa
                     '<li>I do not have any reason to suspect that my goods could be used to make chemical, biological or nuclear weapons</li>'
                     '</ul>'
                 ),
             ],
             default_button_name='Confirm and continue'),
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
        Form(title='Tell us more about this recipient',
             questions=[
                 TextInput(title='What\'s the end user\'s name?',
                             name='end_user.name'),
                 conditional(individual, TextInput(title='What\'s the end user\'s email address?',
                           name='contact_email')),
                 conditional(individual, TextInput(title='What\'s the end user\'s telephone number?',
                           name='contact_telephone')),
                 conditional(commercial, TextInput(title='What\'s the nature of the end user\'s business?',
                           name='nature_of_business')),
                 conditional(not individual, TextInput(title='What\'s the primary contact\'s name?',
                           name='contact_name')),
                 conditional(not individual, TextInput(title='What\'s the primary contact\'s job title?',
                           name='contact_job_title')),
                 conditional(not individual, TextInput(title='What\'s the primary contact\'s email address?',
                           name='contact_email')),
                 conditional(not individual, TextInput(title='What\'s the primary contact\'s telephone number?',
                           name='contact_telephone')),
                 TextInput(title='Enter the end user\'s web address?',
                           name='end_user.website',
                           optional=True),
                 TextArea(title='What\'s the end user\'s address?',
                          description='This is usually the delivery address or registered office for the person '
                                      'receiving the goods',
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
                          name='reasoning',
                          extras={
                              'max_length': 2000,
                          }),
                 TextArea(title='Is there any other information you can provide about this user?',
                          description='This can help to speed up the query and give you a more accurate result',
                          optional=True,
                          name='note',
                          extras={
                              'max_length': 2000,
                          }),
                 HiddenField('validate_only', False),
             ],
             default_button_name='Submit')])


def copy_end_user_advisory_form(individual, commercial):
    return FormGroup([
        Form(title='Tell us more about this recipient',
             questions=[
                 TextInput(title='What\'s the end user\'s name?',
                           name='end_user.name'),
                 conditional(individual, TextInput(title='What\'s the end user\'s email address?',
                                                   name='contact_email')),
                 conditional(individual, TextInput(title='What\'s the end user\'s telephone number?',
                                                   name='contact_telephone')),
                 conditional(commercial, TextInput(title='What\'s the nature of the end user\'s business?',
                                                   name='nature_of_business')),
                 conditional(not individual, TextInput(title='What\'s the primary contact\'s name?',
                                                       name='contact_name')),
                 conditional(not individual, TextInput(title='What\'s the primary contact\'s job title?',
                                                       name='contact_job_title')),
                 conditional(not individual, TextInput(title='What\'s the primary contact\'s email address?',
                                                       name='contact_email')),
                 conditional(not individual, TextInput(title='What\'s the primary contact\'s telephone number?',
                                                       name='contact_telephone')),
                 TextInput(title='Enter the end user\'s web address?',
                           name='end_user.website',
                           optional=True),
                 TextArea(title='What\'s the end user\'s address?',
                          description='This is usually the delivery address or registered office for the person '
                                      'receiving the goods',
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
                          name='reasoning',
                          extras={
                              'max_length': 2000,
                          }),
                 TextArea(title='Is there any other information you can provide about this user?',
                          description='This can help to speed up the query and give you a more accurate result',
                          optional=True,
                          name='note',
                          extras={
                              'max_length': 2000,
                          }),
                 HiddenField('validate_only', False),
             ],
             default_button_name='Submit'),
    ])


def end_user_advisory_success_page(request, query_reference):
    return success_page(request=request,
                        title='Query sent successfully',
                        secondary_title='Your reference code: ' + reference_code(query_reference),
                        description='The Department for International Trade usually takes two '
                                    'working days to check an importer.',
                        what_happens_next=['You\'ll receive an email from DIT when your check is finished.'],
                        links={
                            'View your list of end user advisories': reverse_lazy('end_users:end_users'),
                            'Apply for another advisory': reverse_lazy('end_users:apply'),
                            'Return to Exporter Hub': reverse_lazy('core:hub'),
                        })
