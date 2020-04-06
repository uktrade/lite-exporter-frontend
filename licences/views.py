from django.shortcuts import render
from django.views.generic import TemplateView

from core.services import get_control_list_entries, get_countries
from licences.services import get_licences
from lite_content.lite_exporter_frontend.licences import LicencesList
from lite_forms.components import FiltersBar, TextInput, HiddenField, Select, Checkboxes, Option


class ApplicationsList(TemplateView):
    def get(self, request, **kwargs):
        page = int(request.GET.get("page", 1))
        licence_type = request.GET.get("licence_type")

        licences = get_licences(request, **request.GET)

        filters = FiltersBar(
            [
                TextInput(name="reference", title=LicencesList.Filters.REFERENCE,),
                Select(
                    name="clc",
                    title=LicencesList.Filters.CLC,
                    options=get_control_list_entries(request, convert_to_options=True),
                ),
                Select(
                    name="country",
                    title=LicencesList.Filters.DESTINATION_COUNTRY,
                    options=get_countries(request, convert_to_options=True),
                ),
                TextInput(name="end_user", title=LicencesList.Filters.DESTINATION_NAME,),
                Checkboxes(
                    name="active_only",
                    options=[Option(key=True, value=LicencesList.Filters.ACTIVE)],
                    classes=["govuk-checkboxes--small"],
                ),
                HiddenField(name="licence_type", value=licence_type),
                HiddenField(name="page", value=page),
            ]
        )

        context = {
            "licences": licences,
            "page": page,
            "filters": filters,
        }
        return render(request, "licences/licences.html", context)
