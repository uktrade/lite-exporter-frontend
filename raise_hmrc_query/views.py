from django.shortcuts import render

from django.views.generic import TemplateView

from core.helpers import convert_dict_to_query_params
from raise_hmrc_query.services import get_organisations


class SelectAnOrganisation(TemplateView):
    def get(self, request, *args, **kwargs):
        name = request.GET.get('name', '').strip()
        params = {'page': int(request.GET.get('page', 1)),
                  'name': name}
        organisations = get_organisations(request, org_type='hmrc', **params)

        context = {
            'organisations': organisations,
            'params': params,
            'page': params.pop('page'),
            'params_str': convert_dict_to_query_params(params)
        }
        return render(request, 'raise_hmrc_query/select_organisation.html', context)
