from operator import itemgetter

from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from applications.forms.countries import countries_form, contract_type_form, contract_type_per_country_form
from applications.forms.locations import (
    which_location_form,
    new_location_form,
    external_locations_form,
    add_external_location,
    Locations,
    sites_form,
)
from applications.helpers.countries import get_countries_missing_contract_types, prettify_country_data
from applications.helpers.validators import (
    validate_external_location_choice,
    validate_and_update_goods_location_choice,
    validate_contract_type_countries_choice,
)
from applications.services import (
    get_application,
    get_application_countries,
    post_application_countries,
    put_contract_type_for_country,
    get_application_countries_and_contract_types,
)
from core.services import (
    get_sites_on_draft,
    post_sites_on_draft,
    post_external_locations,
    get_external_locations_on_draft,
    post_external_locations_on_draft,
    delete_external_locations_from_draft,
    get_country,
)
from lite_forms.views import SingleFormView


class GoodsLocation(TemplateView):
    def get(self, request, **kwargs):
        application_id = str(kwargs["pk"])
        application = get_application(request, application_id)

        if not application["goods_locations"]:
            return redirect(reverse_lazy("applications:edit_location", kwargs={"pk": application_id}))

        return render(request, "applications/goods-locations/goods-locations.html", {"application": application})


class EditGoodsLocation(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        application = get_application(request, self.object_pk)
        self.form = which_location_form(self.object_pk, application.sub_type)
        self.action = validate_and_update_goods_location_choice
        self.data = {"choice": Locations.DEPARTED if application.get("have_goods_departed") else ""}

        if application.status == "submitted":
            if application["goods_locations"]:
                return reverse_lazy("applications:location", kwargs={"pk": self.object_pk})
            elif application["sites"]:
                return reverse_lazy("applications:existing_sites", kwargs={"pk": self.object_pk})

    def get_success_url(self):
        choice = self.get_validated_data()["choice"]
        if choice == Locations.EXTERNAL:
            return reverse_lazy("applications:select_add_external_location", kwargs={"pk": self.object_pk})
        elif choice == Locations.ORGANISATION:
            return reverse_lazy("applications:existing_sites", kwargs={"pk": self.object_pk})
        elif choice == Locations.DEPARTED:
            return reverse_lazy("applications:task_list", kwargs={"pk": self.object_pk})


class SelectAddExternalLocation(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.form = add_external_location()
        self.action = validate_external_location_choice

    def get_success_url(self):
        choice = self.get_validated_data()["choice"]
        if choice == "new":
            return reverse_lazy("applications:add_external_location", kwargs={"pk": self.object_pk})
        else:
            return reverse_lazy("applications:add_preexisting_external_location", kwargs={"pk": self.object_pk})


class ExistingSites(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        application = get_application(request, self.object_pk)

        if application.status == "submitted" and not application["goods_locations"]["type"] == "sites":
            raise Http404

        self.data, _ = get_sites_on_draft(request, self.object_pk)
        self.form = sites_form(request, application.type_reference)
        self.action = post_sites_on_draft
        self.success_url = reverse_lazy("applications:location", kwargs={"pk": self.object_pk})


class AddExternalLocation(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        application = get_application(request, self.object_pk)
        self.form = new_location_form(application.type_reference)
        self.action = post_external_locations
        self.success_url = reverse_lazy("applications:location", kwargs={"pk": self.object_pk})


class RemoveExternalLocation(TemplateView):
    def get(self, request, **kwargs):
        draft_id = str(kwargs["pk"])
        ext_loc_id = str(kwargs["ext_loc_pk"])
        delete_external_locations_from_draft(request, draft_id, ext_loc_id)

        return redirect(reverse_lazy("applications:location", kwargs={"pk": draft_id}))


class AddExistingExternalLocation(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        application = get_application(request, self.object_pk)
        self.data, _ = get_external_locations_on_draft(request, self.object_pk)
        self.form = external_locations_form(request, application.type_reference)
        self.action = post_external_locations_on_draft
        self.success_url = reverse_lazy("applications:location", kwargs={"pk": self.object_pk})


class Countries(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.data = {"countries": get_application_countries(request, self.object_pk)}
        self.form = countries_form(self.object_pk)
        self.action = post_application_countries

    def get_success_url(self):
        countries_without_contract_type = get_countries_missing_contract_types(self.request, self.object_pk)
        if not countries_without_contract_type:
            return reverse_lazy("applications:countries_summary", kwargs={"pk": self.object_pk})
        else:
            return reverse_lazy("applications:choose_contract_type", kwargs={"pk": self.object_pk})


class ChooseContractType(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.form = contract_type_form()
        self.action = validate_contract_type_countries_choice

    def get_success_url(self):
        choice = self.get_validated_data()["choice"]
        countries_without_contract_type = get_countries_missing_contract_types(self.request, self.object_pk)

        if choice == "all":
            return reverse_lazy("applications:add_contract_type", kwargs={"pk": self.object_pk, "country": "all"})
        if countries_without_contract_type:
            return reverse_lazy(
                "applications:add_contract_type",
                kwargs={"pk": self.object_pk, "country": countries_without_contract_type[0]["id"]},
            )
        else:
            # Redirect to the summary page if a country has been removed
            return reverse_lazy("applications:countries_summary", kwargs={"pk": self.object_pk})


class AddContractTypes(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.action = put_contract_type_for_country
        current_country = self.kwargs["country"]
        selected_countries = get_application_countries(self.request, self.object_pk)
        data_for_current_country = [
            country_entry
            for country_entry in get_application_countries_and_contract_types(self.request, self.object_pk)
            if country_entry["country"]["id"] == current_country
        ]
        self.data = (
            {
                "contract_types": data_for_current_country[0]["contract_types"],
                "other_contract_type_text": data_for_current_country[0]["other_contract_type_text"],
            }
            if data_for_current_country
            else {}
        )

        if current_country != "all":
            country_name = get_country(request, current_country)["name"]
            if country_name not in str(selected_countries):
                return render(request, "404.html")
            self.form = contract_type_per_country_form([current_country], country_name)
        else:
            selected_countries_ids = [country["id"] for country in selected_countries]
            self.form = contract_type_per_country_form(selected_countries_ids, "all the countries")

    def get_success_url(self):
        selected_countries_without_contract_types = get_countries_missing_contract_types(self.request, self.object_pk)

        # Go through all countries without contract types and render the form again allowing the user to select them
        if selected_countries_without_contract_types:
            next_country = selected_countries_without_contract_types[0]["id"]
            return reverse_lazy(
                "applications:add_contract_type", kwargs={"pk": self.object_pk, "country": next_country}
            )
        else:
            return reverse_lazy("applications:countries_summary", kwargs={"pk": self.object_pk})


class CountriesAndContractTypesSummary(TemplateView):
    def get(self, request, **kwargs):
        object_pk = kwargs["pk"]
        countries_data = get_application_countries_and_contract_types(request, object_pk)
        countries = [
            {
                "country_id": country_entry["country"]["id"],
                "country_name": country_entry["country"]["name"],
                "contract_types": country_entry["contract_types"],
                "other_contract_type_text": country_entry["other_contract_type_text"],
            }
            for country_entry in countries_data
        ]

        prettified_countries = prettify_country_data(sorted(countries, key=itemgetter("country_name")))
        context = {
            "application_id": str(object_pk),
            "countries": prettified_countries,
        }
        return render(request, "applications/goods-locations/destinations-summary-list.html", context)


class StaticDestinations(TemplateView):
    # To be used for OIELs where all countries are preselected and non-modifiable by the user
    def get(self, request, **kwargs):
        application_id = str(kwargs["pk"])
        application = get_application(request, application_id)
        goodstype_category = None

        if application.get("goodstype_category"):
            goodstype_category = application.get("goodstype_category").get("key")
            goodstype_category_label = application.get("goodstype_category").get("value")

        context = {
            "application_id": application_id,
            "countries": get_application_countries(request, application_id),
            "goodstype_category": goodstype_category,
            "goodstype_category_label": goodstype_category_label,
        }
        return render(request, "applications/goods-locations/static-all-destinations.html", context)
