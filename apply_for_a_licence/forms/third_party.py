from lite_forms.components import RadioButtons, Form, Option, FormGroup

from apply_for_a_licence.forms.end_user import third_parties_standard_form

option_list = {
    'agent': 'Agent or broker',
    'intermediate_consignee': 'Intermediate consignee',
    'submitter': 'Authorised submitter',
    'consultant': 'Consultant',
    'contact': 'Contact',
    'exporter': 'Exporter'
}


def third_party_forms():
    third_party_form = third_parties_standard_form()
    options = [Option(key, value) for key, value in option_list.items()]
    options.append(Option('other', 'Other', show_or=True))
    third_party_type = Form(title='What type of third party would you like to add?',
                            questions=[
                                RadioButtons('sub_type', options=options)
                            ],
                            default_button_name='Continue')
    third_party_form[0] = third_party_type
    return FormGroup(third_party_form)
