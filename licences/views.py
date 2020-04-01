from django.shortcuts import render
from django.views.generic import TemplateView

from core.helpers import convert_dict_to_query_params
from licences.services import get_licences


class ApplicationsList(TemplateView):
    def get(self, request, **kwargs):
        params = {"page": int(request.GET.get("page", 1)), "type": request.GET.get("type", "licence")}
        licences = get_licences(request, convert_dict_to_query_params(params))

        context = {
            "licences": licences,
            "params": params,
            "page": params.pop("page"),
        }
        return render(request, "licences/licences.html", context)
