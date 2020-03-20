from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView

from core.services import get_organisation
from lite_forms.generators import form_page
from lite_forms.helpers import flatten_data, nest_data
from lite_forms.views import MultiFormView
from organisation.sites.forms import edit_site_form, new_site_forms
from organisation.sites.services import get_site, post_sites, put_site, get_sites
from organisation.views import OrganisationView


class Sites(OrganisationView):
    template_name = "sites/index"

    def get_additional_context(self):
        return {"sites": get_sites(self.request, self.organisation_id)}


class NewSite(MultiFormView):
    def init(self, request, **kwargs):
        self.object_pk = request.user.organisation
        self.forms = new_site_forms(request)
        self.action = post_sites

    def get_success_url(self):
        pk = self.get_validated_data()["site"]["id"]
        return reverse("organisation:sites:site", kwargs={"pk": pk})


class ViewSite(TemplateView):
    def get(self, request, *args, **kwargs):
        organisation_id = str(request.user.organisation)
        site = get_site(request, organisation_id, kwargs["pk"])
        organisation = get_organisation(request, organisation_id)

        context = {
            "site": site,
            "organisation": organisation,
        }
        return render(request, "organisation/sites/site.html", context)


class EditSite(TemplateView):
    organisation_id = None
    site = None
    form = None

    def dispatch(self, request, *args, **kwargs):
        self.organisation_id = str(request.user.organisation)
        self.site = get_site(request, self.organisation_id, str(kwargs["pk"]))
        self.site["address"]["country"] = self.site["address"]["country"]["id"]
        self.form = edit_site_form(self.site)

        return super(EditSite, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        return form_page(request, self.form, data=flatten_data(self.site))

    def post(self, request, **kwargs):
        validated_data, _ = put_site(request, self.organisation_id, str(kwargs["pk"]), json=nest_data(request.POST))

        if "errors" in validated_data:
            validated_data["errors"] = flatten_data(validated_data["errors"])
            return form_page(request, self.form, data=request.POST, errors=validated_data["errors"])

        return redirect(reverse_lazy("organisation:sites:site", kwargs={"pk": kwargs["pk"]}))
