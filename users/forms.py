from django.urls import reverse_lazy

from libraries.forms.components import Question, Form, InputType, BackLink

_questions = [
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
]

_back_link = BackLink('Back to Users', reverse_lazy('users:users'))

form = Form(title='Add a member to your organisation',
            description='',
            questions=_questions,
            back_link=_back_link)

edit_form = Form(title='Edit member',
                 description='',
                 questions=_questions,
                 back_link=_back_link)
