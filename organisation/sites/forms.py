from conf.constants import Permissions
from lite_content.lite_exporter_frontend import strings, generic
from django.urls import reverse_lazy

from lite_content.lite_exporter_frontend.sites import AddSiteForm
from lite_forms.common import address_questions, foreign_address_questions
from lite_forms.components import (
    Heading,
    BackLink,
    Form,
    TextInput,
    RadioButtons,
    Option,
    FormGroup,
    HiddenField,
    Checkboxes,
    Filter,
)
from lite_forms.helpers import conditional
from lite_forms.styles import HeadingStyle

from core.services import get_countries, get_organisation_users


def new_site_forms(request):
    in_uk = request.POST.get("location", "").lower() == "united_kingdom"

    return FormGroup(
        [
            Form(
                caption="Step 1 of 3",
                title="Where is your site based?",
                description="",
                questions=[
                    RadioButtons(
                        name="location",
                        options=[
                            Option("united_kingdom", "In the United Kingdom"),
                            Option("abroad", "Outside the United Kingdom"),
                        ],
                    )
                ],
                default_button_name=generic.CONTINUE,
                back_link=BackLink(AddSiteForm.BACK_LINK, reverse_lazy("organisation:sites:sites")),
            ),
            Form(
                caption="Step 2 of 3",
                title="Site details",
                questions=[
                    TextInput(title="Name", name="name"),
                    Heading(
                        conditional(
                            in_uk, "Where in the United Kingdom is your site based?", "Where is your site based?"
                        ),
                        HeadingStyle.M,
                    ),
                    *conditional(
                        in_uk, address_questions(None), foreign_address_questions(get_countries(None, True, ["GB"])),
                    ),
                    HiddenField("validate_only", True),
                ],
                default_button_name=generic.CONTINUE,
            ),
            Form(
                caption="Step 3 of 3",
                title="Assign users to the site (optional)",
                description="Users with the permission to manage sites will still be able to access the site. You can still assign users later.",
                questions=[
                    Filter(placeholder="Filter users"),
                    Checkboxes(
                        name="users[]",
                        options=get_organisation_users(
                            request,
                            request.user.organisation,
                            {"disable_pagination": True, "exclude_permission": Permissions.ADMINISTER_SITES},
                            True,
                        ),
                    ),
                    HiddenField("validate_only", False),
                ],
                javascript_imports=["/assets/javascripts/filter-checkbox-list.js"],
                default_button_name=generic.SAVE_AND_CONTINUE,
            ),
        ]
    )


def edit_site_name_form(site):
    return Form(
        title=strings.sites.SitesPage.EDIT + site["name"],
        questions=[TextInput(title="Name", name="name"),],
        back_link=BackLink(
            strings.sites.SitesPage.BACK_TO + site["name"],
            reverse_lazy("organisation:sites:site", kwargs={"pk": site["id"]}),
        ),
    )


def edit_site_address_form(site):
    return Form(
        title=strings.sites.SitesPage.EDIT + site["name"],
        questions=[*address_questions(get_countries(None, True)),],
        back_link=BackLink(
            strings.sites.SitesPage.BACK_TO + site["name"],
            reverse_lazy("organisation:sites:site", kwargs={"pk": site["id"]}),
        ),
    )
