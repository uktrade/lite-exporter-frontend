from django import forms


class NewApplicationForm1(forms.Form):
    name = forms.CharField(label='Name/Reference',
                           required=False,
						   widget = forms.TextInput(
            			   	   attrs = {'class': 'govuk-input govuk-input--width-20'}
        				   ))


class NewApplicationForm2(forms.Form):
    message = forms.CharField(label='Testy mc testface',
                              help_text='Bananan',
                              widget=forms.Textarea,
                              required=False)
