from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from applications.forms.countries import countries_form
from applications.forms.location import (
    which_location_form,
    new_location_form,
    external_locations_form,
    add_external_location,
    Locations,
)
from applications.forms.sites import sites_form
from applications.helpers.validators import validate_external_location_choice, validate_and_update_goods_location_choice
from applications.services import get_application, get_application_countries, post_application_countries
from core.services import (
    get_sites_on_draft,
    post_sites_on_draft,
    post_external_locations,
    get_external_locations_on_draft,
    post_external_locations_on_draft,
    delete_external_locations_from_draft,
)
from lite_forms.generators import form_page
from lite_forms.submitters import submit_single_form
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
        self.form = which_location_form(self.object_pk, application.get_application_sub_type())
        self.action = validate_and_update_goods_location_choice
        self.data = {"choice": Locations.DEPARTED if application.get("have_goods_departed") else ""}

        if application.get_status() == "submitted":
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


class ExistingSites(TemplateView):
    def get(self, request, **kwargs):
        application_id = str(kwargs["pk"])
        application = get_application(request, application_id)
        response, _ = get_sites_on_draft(request, application_id)

        if application.get_status() == "submitted" and not response["sites"]:
            raise Http404

        return form_page(request, sites_form(request), data=response)

    def post(self, request, **kwargs):
        draft_id = str(kwargs["pk"])
        data = {"sites": request.POST.getlist("sites")}

        response, status_code = post_sites_on_draft(request, draft_id, data)

        if status_code != 201:
            return form_page(request, sites_form(request), errors=response.get("errors"), data=data)

        return redirect(reverse_lazy("applications:location", kwargs={"pk": draft_id}))


# External Locations

class AddExternalLocation(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        application = get_application(request, self.object_pk)
        self.form = new_location_form(application.get_application_type_reference())
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
        self.form = external_locations_form(request, application.get_application_type_reference())
        self.action = post_external_locations_on_draft
        self.success_url = reverse_lazy("applications:location", kwargs={"pk": self.object_pk})


# Countries


class Countries(TemplateView):
    def get(self, request, **kwargs):
        draft_id = str(kwargs["pk"])
        countries = {"countries": get_application_countries(request, draft_id)}

        return form_page(request, countries_form(draft_id), data=countries)

    def post(self, request, **kwargs):
        draft_id = str(kwargs["pk"])

        data = {"countries": request.POST.getlist("countries")}

        response, _ = submit_single_form(
            request, countries_form(draft_id), post_application_countries, object_pk=draft_id, override_data=data
        )

        if response:
            return response

        return redirect(reverse_lazy("applications:task_list", kwargs={"pk": draft_id}))
