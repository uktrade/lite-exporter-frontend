from form.models import Section, Form, Question, InputType, ArrayQuestion, Option

section1 = Section("Application Information", "sd", [
	Form("Enter a name or reference for your application", "This can make it easier to find in the future.", [
		Question(title='',
				 description='',
				 input_type=InputType.INPUT,
				 name='name'),
	]),
	Form("Control code", "This can make it easier to find in the future.", [
		Question(title='',
				 description='',
				 input_type=InputType.INPUT,
				 name='control_code'),
	]),
	Form("Destination", "it might be over soon", [
		Question(title='',
				 description='',
				 input_type=InputType.INPUT,
				 name='destination'),
	]),
	Form("Usage", "it might be over soon", [
		Question(title='',
				 description='',
				 input_type=InputType.INPUT,
				 name='usage'),
	]),
	Form("Activity", "it might be over soon", [
		Question(title='',
				 description='',
				 input_type=InputType.INPUT,
				 name='activity'),
	]),
])
