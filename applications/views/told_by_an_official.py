from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from lite_forms.generators import form_page
from lite_forms.submitters import submit_single_form

from applications.forms.reference_name import reference_name_form
from applications.forms.told_by_an_official import told_by_an_official_form
from applications.services import get_application, put_application


class ApplicationEditToldByAnOfficial(TemplateView):

    application_id = None
    application = None
    form = told_by_an_official_form()

    def dispatch(self, request, *args, **kwargs):
        self.application_id = str(kwargs['pk'])
        self.application = get_application(request, self.application_id)

        return super(ApplicationEditToldByAnOfficial, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        data = {
            'have_you_been_informed': 'yes' if self.application['reference_number_on_information_form'] else 'no',
            'reference_number_on_information_form': self.application['reference_number_on_information_form'],
        }

        return form_page(request, self.form, data=data)

    def post(self, request, **kwargs):
        # Delete the reference_number_on_information_form key if have_you_been_informed is set to no
        data = {}
        if request.POST['have_you_been_informed'] == 'no':
            data = {'reference_number_on_information_form': None}

        response, response_data = submit_single_form(request, self.form, put_application, pk=self.application_id,
                                                     override_data=data)

        # If there are more forms to go through, continue
        if response:
            return response

        return redirect(reverse_lazy('applications:edit', kwargs={'pk': self.application_id}))
