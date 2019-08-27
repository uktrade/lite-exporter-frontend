from lite_forms.components import HTMLBlock, Form, HiddenField, SideBySideSection, Select, TextInput


def preexisting_good_form(id, description, control_code, part_number, units):
    return Form('Add a pre-existing good to your application', '', [
        HTMLBlock('<div class="govuk-inset-text">'
                  '<p><span style="opacity: 0.6;">Description:</span> ' + description + '</p>'
                                                                                        '<p><span style="opacity: 0.6;">Control Code:</span> ' + control_code + '</p>'
                                                                                                                                                                '<p><span style="opacity: 0.6;">Part Number:</span> ' + part_number + '</p>'
                                                                                                                                                                                                                                      '</div>'),
        HiddenField(name='good_id',
                    value=id),
        TextInput(title='What\'s the value of your goods?',
                  name='value'),
        SideBySideSection(questions=[
            TextInput(title='Quantity',
                      name='quantity'),
            Select(title='Unit of Measurement',
                   name='unit',
                   options=units)
        ]),
    ], javascript_imports=[
        '/assets/javascripts/specific/add_good.js'
    ])
