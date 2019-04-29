from core.form_components import Form, Question, InputType

form = Form(title='Add User', description='', caption='', questions=[
    Question(title='First name',
             description='',
             input_type=InputType.INPUT,
             name='first_name'),
    Question(title='Last name',
             description='',
             input_type=InputType.INPUT,
             name='last_name'),
    Question(title='Email',
             description='',
             input_type=InputType.INPUT,
             name='email'),
    Question(title='Password',
             description='',
             input_type=InputType.PASSWORD,
             name='password')
])
