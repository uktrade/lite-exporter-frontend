from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from conf.constants import Permissions
from lite_forms.generators import form_page
from lite_forms.helpers import flatten_data, nest_data

from core.services import get_organisation
from roles.services import get_user_permissions
from sites.forms import new_site_form, edit_site_form
from sites.services import get_sites, get_site, post_sites, put_site


class Sites(TemplateView):
    def get(self, request, **kwargs):
        organisation_id = str(request.user.organisation)
        sites = get_sites(request, organisation_id)
        organisation = get_organisation(request, organisation_id)
        user_permissions = get_user_permissions(request)

        users, roles = False, False
        if Permissions.ADMINISTER_USERS in user_permissions:
            users = True

        if Permissions.EXPORTER_ADMINISTER_ROLES in user_permissions:
            roles = True


        context = {
            "title": "Sites - " + organisation["name"],
            "sites": sites,
            "organisation": organisation,
            "can_administer_roles": roles,
            "can_administer_users": users
        }
        return render(request, "sites/index.html", context)


class NewSite(TemplateView):
    form = None

    def dispatch(self, request, *args, **kwargs):
        self.form = new_site_form()

        return super(NewSite, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        return form_page(request, self.form)

    def post(self, request, **kwargs):
        organisation_id = str(request.user.organisation)
        validated_data, _ = post_sites(request, organisation_id, nest_data(request.POST))

        if "errors" in validated_data:
            validated_data["errors"] = flatten_data(validated_data["errors"])
            return form_page(request, self.form, data=request.POST, errors=validated_data["errors"])

        return redirect(reverse_lazy("sites:sites"))


class EditSite(TemplateView):
    organisation_id = None
    site = None
    form = None

    def dispatch(self, request, *args, **kwargs):
        self.organisation_id = str(request.user.organisation)
        self.site, _ = get_site(request, self.organisation_id, str(kwargs["pk"]))
        self.site["site"]["address"]["country"] = self.site["site"]["address"]["country"]["id"]
        self.form = edit_site_form("Edit " + self.site["site"]["name"])

        return super(EditSite, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        return form_page(request, self.form, data=flatten_data(self.site.get("site")))

    def post(self, request, **kwargs):
        validated_data, _ = put_site(request, self.organisation_id, str(kwargs["pk"]), json=nest_data(request.POST))

        if "errors" in validated_data:
            validated_data["errors"] = flatten_data(validated_data["errors"])
            return form_page(request, self.form, data=request.POST, errors=validated_data["errors"])

        return redirect(reverse_lazy("sites:sites"))
