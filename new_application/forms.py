from core.form_components import Section, Form, Question, InputType, HTMLBlock, HiddenField, ArrayQuestion, Option

section1 = Section("Application Information", "", [
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


def preexisting_good_form(id, description, control_code, part_number):
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
        Question(title='Quantity',
                 description='',
                 input_type=InputType.INPUT,
                 name='quantity'),
        ArrayQuestion(title='Unit of Measurement',
                      description='',
                      input_type=InputType.SELECT,
                      name='unit',
                      data=[
                          Option(key='GRM',
                                 value='Gram(s)'),
                          Option(key='KGM',
                                 value='Kilogram(s)'),
                          Option(key='NAR',
                                 value='Number of articles'),
                          Option(key='MTK',
                                 value='Square Metre(s)'),
                          Option(key='MTR',
                                 value='Metre(s)'),
                          Option(key='LTR',
                                 value='Litre(s)'),
                          Option(key='MTQ',
                                 value='Cubic Metre(s)'),
                      ])
    ])
