from conf.settings import env
from core.form_components import Form, Question, InputType, ArrayQuestion, Option

form = Form(title='Add Good', description='', caption='Business Name Goes Here', questions=[
    Question(title='Description of good',
             description='This can make it easier to find your good later',
             input_type=InputType.TEXTAREA,
             name='description'),
    ArrayQuestion(title='Is your good controlled?',
                  description='If you don\'t know you can use <a class="govuk-link" href="' + env('PERMISSIONS_FINDER_URL') + '">Permissions Finder</a>.',
                  input_type=InputType.RADIOBUTTONS,
                  name='know_your_control_code',
                  data=[
                      Option(key='yes',
                             value='Yes',
                             show_pane='pane_control_code'),
                      Option(key='no',
                             value='No')
                  ]),
    Question(title='Control Code',
             description='If your good is controlled, enter its control code. For example, ML1a.',
             input_type=InputType.INPUT,
             name='control_code'),
    ArrayQuestion(title='Is your good intended to be incorporated into an end product?',
                  description='',
                  input_type=InputType.RADIOBUTTONS,
                  name='into_end_product',
                  data=[
                      Option(key='yes',
                             value='Yes'),
                      Option(key='no',
                             value='No')
                  ]),
    Question(title='Part Number',
             description='',
             input_type=InputType.INPUT,
             name='part_number'),
])
