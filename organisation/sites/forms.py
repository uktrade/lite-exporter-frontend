from conf.constants import Permissions
from lite_content.lite_exporter_frontend import strings
from django.urls import reverse_lazy

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
                default_button_name="Continue",
                back_link=BackLink("Back to sites", reverse_lazy("organisation:sites:sites")),
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
                default_button_name="Save and continue",
            ),
            Form(
                caption="Step 3 of 3",
                title="Assign users to the site (optional)",
                description="Users with the permission to manage sites will still be able to access the site",
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
                default_button_name="Save and continue",
            ),
        ]
    )


def edit_site_form(site):
    return Form(
        title=strings.sites.SitesPage.EDIT + site["name"],
        questions=[
            TextInput(title="Name", name="name"),
            Heading("Address", HeadingStyle.M),
            *address_questions(get_countries(None, True)),
        ],
        back_link=BackLink(
            strings.sites.SitesPage.BACK_TO + site["name"],
            reverse_lazy("organisation:sites:site", kwargs={"pk": site["id"]}),
        ),
    )
