from libraries.forms.components import Section, Form, Question, InputType, HTMLBlock, HiddenField, SideBySideSection, \
    ArrayQuestion, Option, DetailComponent, Button

section1 = Section("Application Information", "", [
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
                                                        'exporting and doing business abroad</a>.',)
    ], buttons=[
        Button('Save and continue', 'submit')
    ]),
    Form("Enter a name or reference for your application", "This can make it easier to find in the future.", [
        Question(title='',
                 description='',
                 input_type=InputType.INPUT,
                 name='name'),
    ]),
    Form("Destination", "", [
        Question(title='',
                 description='',
                 input_type=InputType.INPUT,
                 name='destination'),
    ]),
    Form("Usage", "", [
        Question(title='',
                 description='',
                 input_type=InputType.INPUT,
                 name='usage'),
    ]),
    Form("Activity", "", [
        Question(title='',
                 description='',
                 input_type=InputType.INPUT,
                 name='activity'),
    ]),
])


def preexisting_good_form(id, description, control_code, part_number, units):
    return Form('Add a pre-existing good to your application', '', [
        HTMLBlock('<div class="govuk-inset-text">'
                  '<p><span style="opacity: 0.6;">Description:</span> ' + description + '</p>'
                                                                                        '<p><span style="opacity: 0.6;">Control Code:</span> ' + control_code + '</p>'
                                                                                                                                                                '<p><span style="opacity: 0.6;">Part Number:</span> ' + part_number + '</p>'
                                                                                                                                                                                                                                      '</div>'),
        HiddenField(name='good_id',
                    value=id),
        Question(title='What\'s the value of your goods?',
                 description='',
                 input_type=InputType.CURRENCY,
                 name='value'),
        SideBySideSection(questions=[
            Question(title='Quantity',
                     description='',
                     input_type=InputType.INPUT,
                     name='quantity'),
            ArrayQuestion(title='Unit of Measurement',
                          description='',
                          input_type=InputType.SELECT,
                          name='unit',
                          data=units)
        ]),
    ], javascript_imports=[
        '/assets/javascripts/specific/add_good.js'
    ])
