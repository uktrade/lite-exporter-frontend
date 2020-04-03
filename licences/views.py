from django.shortcuts import render
from django.views.generic import TemplateView

from core.helpers import convert_dict_to_query_params
from core.services import get_control_list_entries, get_countries
from licences.services import get_licences
from lite_content.lite_exporter_frontend.licences import LicencesList
from lite_forms.components import FiltersBar, TextInput, HiddenField, Select, Checkboxes, Option


class ApplicationsList(TemplateView):
    def get(self, request, **kwargs):
        params = {
            "page": int(request.GET.get("page", 1)),
            "type": request.GET.get("type", "licence"),
            "reference": request.GET.get("reference"),
            "clc": request.GET.get("clc"),
            "country": request.GET.get("country"),
            "end_user": request.GET.get("end_user"),
            "active_only": request.GET.get("active_only"),
        }
        licences = get_licences(request, convert_dict_to_query_params(params))

        filters = FiltersBar(
            [
                TextInput(name="reference", title=LicencesList.Filters.REFERENCE,),
                Select(name="clc", title=LicencesList.Filters.CLC, options=get_control_list_entries(request, convert_to_options=True)),
                Select(name="country", title=LicencesList.Filters.DESTINATION_COUNTRY, options=get_countries(request, convert_to_options=True)),
                TextInput(name="end_user", title=LicencesList.Filters.DESTINATION_NAME,),
                Checkboxes(
                    name="active_only",
                    options=[Option(key=True, value=LicencesList.Filters.ACTIVE)],
                    classes=["govuk-checkboxes--small"],
                ),
                HiddenField(name="type", value=params["type"]),
                HiddenField(name="page", value=params["page"]),
            ]
        )

        context = {
            "licences": licences,
            "page": params.pop("page"),
            "filters": filters,
        }
        return render(request, "licences/licences.html", context)
