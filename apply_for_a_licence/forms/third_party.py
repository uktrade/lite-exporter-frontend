from lite_forms.components import RadioButtons, Form, Option, FormGroup

from apply_for_a_licence.forms.end_user import third_parties_standard_form


def third_party_forms():
    third_party_form = third_parties_standard_form()
    third_party_type = Form(title='What type of third party would you like to add?',
                            questions=[
                                RadioButtons('sub_type',
                                             options=[
                                                 Option('agent', 'Agent'),
                                                 Option('intermediate_consignee', 'Intermediate consignee'),
                                                 Option('authorised_submitter', 'Authorised submitter'),
                                                 Option('consultant', 'Consultant'),
                                                 Option('contact', 'Contact'),
                                                 Option('exporter', 'Exporter (Broker or other party)'),
                                                 Option('other', 'Other', show_or=True),
                                             ]),
                            ],
                            default_button_name='Continue')
    third_party_form[0] = third_party_type
    return FormGroup(third_party_form)
