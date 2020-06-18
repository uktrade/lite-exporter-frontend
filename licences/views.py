from http import HTTPStatus

from django.http import Http404
from django.shortcuts import render
from django.views.generic import TemplateView

from apply_for_a_licence.enums import OpenGeneralExportLicenceTypes
from core.objects import Tab
from core.services import get_control_list_entries, get_countries
from core.services import get_open_general_licences
from licences.helpers import (
    get_potential_ogl_control_list_entries,
    get_potential_ogl_countries,
    get_potential_ogl_sites,
)
from licences.services import get_licences, get_licence, get_nlr_licences
from lite_content.lite_exporter_frontend.licences import LicencesList, LicencePage
from lite_forms.components import (
    FiltersBar,
    TextInput,
    HiddenField,
    Select,
    Checkboxes,
    Option,
    AutocompleteInput,
)
from lite_forms.generators import error_page


class Licences(TemplateView):
    type = None
    data = None
    filters = None
    template = None
    page = 1

    def get_licences(self):
        params = self.request.GET.copy()
        if "licence_type" in params:
            params.pop("licence_type")
        self.data = get_licences(
            self.request, licence_type="licence" if self.type == "licences" else "clearance", **params
        )
        self.filters = [
            TextInput(name="reference", title=LicencesList.Filters.REFERENCE,),
            AutocompleteInput(
                name="clc",
                title=LicencesList.Filters.CLC,
                options=get_control_list_entries(self.request, convert_to_options=True),
            ),
            AutocompleteInput(
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

    def get_no_licence_required(self):
        params = self.request.GET.copy()
        params.pop("licence_type")
        self.data = get_nlr_licences(self.request, **params)
        self.filters = [
            TextInput(name="reference", title=LicencesList.Filters.REFERENCE,),
            AutocompleteInput(
                name="clc",
                title=LicencesList.Filters.CLC,
                options=get_control_list_entries(self.request, convert_to_options=True),
            ),
            AutocompleteInput(
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
        self.template = "nlrs"

    def get_open_general_licences(self):
        params = self.request.GET.copy()
        params.pop("licence_type")
        self.data = get_open_general_licences(self.request, registered=True, **params)
        control_list_entries = get_potential_ogl_control_list_entries(self.data)
        countries = get_potential_ogl_countries(self.data)
        sites = get_potential_ogl_sites(self.data)
        self.filters = [
            TextInput(name="name", title="name"),
            Select(name="case_type", title="type", options=OpenGeneralExportLicenceTypes.as_options(),),
            AutocompleteInput(name="control_list_entry", title="control list entry", options=control_list_entries,),
            AutocompleteInput(name="country", title="country", options=countries),
            Select(name="site", title="site", options=sites,),
            Checkboxes(
                name="active_only",
                options=[Option(key=True, value="Only show active")],
                classes=["govuk-checkboxes--small"],
            ),
        ]
        self.template = "open-general-licences"

    def get(self, request, **kwargs):
        self.type = request.GET.get("licence_type", "licences")
        self.page = int(request.GET.get("page", 1))
        getattr(self, f"get_{self.type}", self.get_licences)()  # Set template properties

        context = {
            "data": self.data,
            "filters": FiltersBar([*self.filters, HiddenField(name="licence_type", value=self.type)]),
            "tabs": [
                Tab("licences", LicencesList.Tabs.LICENCE, "?licence_type=licences"),
                Tab("open_general_licences", LicencesList.Tabs.OGLS, "?licence_type=open_general_licences"),
                Tab("no_licence_required", LicencesList.Tabs.NLR, "?licence_type=no_licence_required"),
                Tab("clearances", LicencesList.Tabs.CLEARANCE, "?licence_type=clearances"),
            ],
            "selected_tab": self.type,
            "reference": request.GET.get("reference", ""),
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
