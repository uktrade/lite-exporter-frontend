from core.form_components import Section, Form, Question, InputType

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
