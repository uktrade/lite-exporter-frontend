from core.form_components import Form, Question, InputType, HelpSection

form = Form("Add Good", "This is an example description", [
    Question(title='Name',
             description='Set a name for your good',
             input_type=InputType.INPUT,
             name='name'),
    Question(title='Control Code',
             description='Set a name for your good',
             input_type=InputType.INPUT,
             name='control_code'),
    Question(title='Quantity',
             description='Set a name for your good',
             input_type=InputType.NUMBER,
             name='quantity'),
    Question(title='Part Number',
             description='Set a name for your good',
             input_type=InputType.INPUT,
             name='part_number'),
], [
    HelpSection(title='Dont know your control code?',
                description='Use Codefinder'),
    HelpSection(title='Dont know your control code?',
                description='Use Codefinder'),
    HelpSection(title='Dont know your control code?',
                description='Use Codefinder'),
])
