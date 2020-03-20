from lite_content.lite_exporter_frontend import strings
from django.urls import reverse_lazy

from lite_forms.common import address_questions, foreign_address_questions
from lite_forms.components import Heading, BackLink, Form, TextInput, RadioButtons, Option, FormGroup, HiddenField
from lite_forms.helpers import conditional
from lite_forms.styles import HeadingStyle

from core.services import get_countries


def new_site_forms(request):
    in_uk = request.POST.get("location", "").lower() == "united_kingdom"

    return FormGroup([
        Form(
            caption="Add a site",
            title="Details",
            description="",
            questions=[
                TextInput(title="Name", name="name"),
                RadioButtons(
                    title="Where is your site based?",
                    name="location",
                    options=[
                        Option("united_kingdom", "In the United Kingdom"),
                        Option("abroad", "Outside the United Kingdom")
                    ]
                )
            ],
            default_button_name="Continue",
            back_link=BackLink("Back to sites", reverse_lazy("organisation:sites:sites")),
        ),
        Form(
            caption="Add a site",
            title="Where in the United Kingdom is your site based?",
            description="",
            questions=[
                *conditional(
                    in_uk,
                    [*address_questions(None),
                     HiddenField("country", "GB")],
                    foreign_address_questions(get_countries(None, True)),
                )
            ],
            default_button_name="Continue"
        )
    ])


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
