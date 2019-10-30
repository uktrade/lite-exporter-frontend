from django.http import Http404
from django.shortcuts import render
from django.views.generic import TemplateView
from lite_forms.generators import form_page

from applications.forms.hmrc import confirm_organisation_form
from applications.libraries.get_hmrc_task_list import get_hmrc_task_list
from core.helpers import convert_dict_to_query_params
from raise_hmrc_query.services import get_organisations, get_organisation


class SelectAnOrganisation(TemplateView):
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
            if organisation:
                organisation = get_organisation(request, request.POST.get('organisation'))
                return form_page(request, confirm_organisation_form(organisation))
            else:
                return self.get(request, show_error=True, *args, **kwargs)
        else:
            # Do an application POST here to create the draft
            # then redirect to the application:edit page for hmrc queries
            return get_hmrc_task_list(request, None)
