from django.shortcuts import render
from django.views.generic import TemplateView

from core.helpers import convert_dict_to_query_params
from licences.services import get_licences
from lite_forms.components import FiltersBar, TextInput, HiddenField


class ApplicationsList(TemplateView):
    def get(self, request, **kwargs):
        params = {
            "page": int(request.GET.get("page", 1)),
            "type": request.GET.get("type", "licence"),
            "reference": request.GET.get("reference"),
        }
        licences = get_licences(request, convert_dict_to_query_params(params))

        filters = FiltersBar([
            TextInput(name="reference", title="Reference",),
            HiddenField(name="type", value=params["type"]),
            HiddenField(name="page", value=params["page"]),
        ])

        context = {
            "licences": licences,
            "page": params.pop("page"),
            "filters": filters,
        }
        return render(request, "licences/licences.html", context)
