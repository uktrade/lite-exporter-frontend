from libraries.forms.components import Form, ArrayQuestion, InputType, Button, DetailComponent, Question, Option, \
    Section

initial_questions = Section('', '', [
    Form('Which export licence do you want to apply for?', 'Select one of the options.', [
        ArrayQuestion(title='',
                      description='',
                      input_type=InputType.RADIOBUTTONS,
                      name='licence_type',
                      data=[
                          Option(key='standard_licence', value='Standard Individual Export Licence (SIEL)',
                                 description='SIELs are specific to the company and the recipient (consignee). '
                                             'They are for a set quantity and set value of goods. '
                                             'You will need to provide support documentation with your application.'),
                          Option(key='open_licence', value='Open Individual Export Licence (OIEL)',
                                 description='OIELs cover long-term projects and repeat business. '
                                             'This is company specific, with no set quantity or value of goods. '
                                             'You will receive compliance audits under this type of licence.'),
                      ]),
        DetailComponent('Help with choosing a licence', 'If you\'re unsure about which licence to select, '
                                                        'then please read the guidance on GOV.UK about licences for '
                                                        '<a class="govuk-link" '
                                                        'href="https://www.gov.uk/starting-to-export/licences">'
                                                        'exporting and doing business abroad</a>.', )
    ], buttons=[
        Button('Save and continue', 'submit')
    ]),
    Form('Do you want to export temporarily or permanently', '', [
        ArrayQuestion(title='',
                      description='',
                      input_type=InputType.RADIOBUTTONS,
                      name='export_type',
                      data=[
                        Option('temporary', 'Temporarily'),
                        Option('permanent', 'Permanently')
                      ]),
    ]),
    Form('Have you been officially informed that you need to apply for a licence?', '', [
        ArrayQuestion(title='',
                      description='',
                      input_type=InputType.RADIOBUTTONS,
                      name='have_you_been_informed',
                      data=[
                        Option('yes', 'Yes', show_pane='pane_reference_number_on_information_form'),
                        Option('no', 'No')
                      ],
                      same_row=True),
        Question(title='What was the reference number if you were provided one?',
                 description='',
                 input_type=InputType.INPUT,
                 name='reference_number_on_information_form',
                 optional=True),
    ]),
])
