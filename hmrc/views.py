from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from applications.forms.hmrc import confirm_organisation_form
from applications.services import post_applications, get_draft_applications
from core.helpers import convert_dict_to_query_params
from core.permissions import is_in_organisation_type
from core.services import get_organisations, get_organisation
from lite_forms.generators import form_page


class DraftsList(TemplateView):

    def dispatch(self, request, *args, **kwargs):
        is_in_organisation_type(request, 'hmrc')
        return super(DraftsList, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        drafts = get_draft_applications(request)

        context = {
            'drafts': drafts
        }
        return render(request, 'hmrc/drafts.html', context)


class SelectAnOrganisation(TemplateView):

    def dispatch(self, request, *args, **kwargs):
        is_in_organisation_type(request, 'hmrc')
        return super(SelectAnOrganisation, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        name = request.GET.get('name', '').strip()
        params = {'page': int(request.GET.get('page', 1)),
                  'name': name}
        organisations = get_organisations(request, org_type='commercial', **params)

        context = {
            'organisations': organisations,
            'params': params,
            'page': params.pop('page'),
            'params_str': convert_dict_to_query_params(params),
            'show_error': kwargs.get('show_error', False)
        }
        return render(request, 'hmrc/select-organisation.html', context)

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        organisation = request.POST.get('organisation')

        if action == 'continue':
            # Return an error if the user hasn't selected an organisation
            if organisation:
                organisation = get_organisation(request, request.POST.get('organisation'))
                return form_page(request, confirm_organisation_form(organisation))
            else:
                return self.get(request, show_error=True, *args, **kwargs)
        else:
            # Create a draft HMRC application
            data = {
                'name': 'HMRC Query',
                'application_type': 'hmrc_query',
                'export_type': 'permanent',
                'reference_number_on_information_form': '',
                'have_you_been_informed': 'no',
                'organisation': organisation
            }

            response, _ = post_applications(request, data)

            return redirect(reverse_lazy('applications:edit', kwargs={'pk': response['id']}))
