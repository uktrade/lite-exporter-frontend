from core.form_components import Form, Question, InputType, HelpSection, ArrayQuestion, Option

form = Form("Add Good", "This is an example description", [
    Question(title='Name',
             description='Set a name for your good',
             input_type=InputType.INPUT,
             name='name'),
    ArrayQuestion(title='Is your good controlled?',
                  description='If you dont know you can use <a href="https://google.com">Permissions Finder</a>',
                  input_type=InputType.RADIOBUTTONS,
                  name='know_your_control_code',
                  data=[
                      Option(key='yes',
                             value='Yes'),
                      Option(key='no',
                             value='No')
                  ]),
    Question(title='Control Code',
             description='',
             input_type=InputType.INPUT,
             name='control_code'),
    Question(title='Quantity',
             description='',
             input_type=InputType.NUMBER,
             name='quantity'),
    Question(title='Part Number',
             description='',
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
