from http import HTTPStatus

from django.http import Http404
from django.shortcuts import render
from django.views.generic import TemplateView

from core.objects import Tab
from core.services import get_control_list_entries, get_countries
from core.services import get_open_general_licences
from licences.services import get_licences, get_licence
from lite_content.lite_exporter_frontend.licences import LicencesList, LicencePage
from lite_forms.components import FiltersBar, TextInput, HiddenField, Select, Checkboxes, Option, AutocompleteInput
from lite_forms.generators import error_page
from organisation.sites.services import get_sites


class Licences(TemplateView):
    type = None
    data = None
    filters = None
    template = None
    page = 1

    def get_licences(self):
        self.data = get_licences(self.request, **self.request.GET)
        self.filters = [
            TextInput(name="reference", title=LicencesList.Filters.REFERENCE,),
            Select(
                name="clc",
                title=LicencesList.Filters.CLC,
                options=get_control_list_entries(self.request, convert_to_options=True),
            ),
            Select(
                name="country",
                title=LicencesList.Filters.DESTINATION_COUNTRY,
                options=get_countries(self.request, convert_to_options=True),
            ),
            TextInput(name="end_user", title=LicencesList.Filters.DESTINATION_NAME,),
            Checkboxes(
                name="active_only",
                options=[Option(key=True, value=LicencesList.Filters.ACTIVE)],
                classes=["govuk-checkboxes--small"],
            ),
        ]
        self.template = "licences"

    def get_open_general_licences(self):
        params = self.request.GET.copy()
        params.pop("licence_type")
        self.data = get_open_general_licences(self.request, registered=True, **params)
        self.filters = [
            TextInput(name="name", title="name"),
            AutocompleteInput(
                name="control_list_entry",
                title="control list entry",
                options=get_control_list_entries(self.request, True),
            ),
            AutocompleteInput(name="country", title="country", options=get_countries(self.request, True)),
            Select(
                name="site",
                title="site",
                options=get_sites(self.request, self.request.user.organisation, convert_to_options=True),
            ),
        ]
        self.template = "open-general-licences"

    def get(self, request, **kwargs):
        self.type = request.GET.get("licence_type")
        self.page = int(request.GET.get("page", 1))
        getattr(self, f"get_{self.type}", self.get_licences)()  # Set template properties

        context = {
            "data": self.data,
            "filters": FiltersBar([*self.filters, HiddenField(name="licence_type", value=self.type)]),
            "tabs": [
                Tab("licences", "OIELs and SIELs", "?licence_type=licences"),
                Tab("open-general-licences", "OGLs", "?licence_type=open_general_licences"),
                Tab("no-licence-required", "NLRs", "?licence_type=no_licence_required"),
                Tab("clearances", "Clearances", "?licence_type=clearances"),
            ],
            "name": request.GET.get("name", ""),
            "row_limit": 3,
        }
        return render(request, f"licences/{self.template}.html", context)


class Licence(TemplateView):
    def get(self, request, pk):
        licence, status_code = get_licence(request, pk)
        if status_code == HTTPStatus.NOT_FOUND:
            return Http404
        elif status_code != HTTPStatus.OK:
            return error_page(request, LicencePage.ERROR)
        return render(request, "licences/licence.html", {"licence": licence})
