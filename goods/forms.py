from core.form_components import Form, Question, InputType, ArrayQuestion, Option

form = Form('Add Good', '', [
    Question(title='Description of good',
             description='This can make it easier to find your good later',
             input_type=InputType.TEXTAREA,
             name='description'),
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
])
