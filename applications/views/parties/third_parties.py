from django.shortcuts import render
from django.views.generic import TemplateView

from applications.forms.third_party import third_party_forms
from applications.services import get_application, post_third_party, delete_third_party
from applications.views.parties.base import SetParty, DeleteParty
from lite_content.lite_exporter_frontend.applications import ThirdPartyForm


class ThirdParties(TemplateView):
    def get(self, request, **kwargs):
        application_id = str(kwargs["pk"])
        application = get_application(request, application_id)

        context = {
            "application": application,
            "third_parties": application["third_parties"],
        }
        return render(request, "applications/parties/third-parties.html", context)


class AddThirdParty(SetParty):
    def __init__(self):
        super().__init__(
            url="applications:third_party_attach_document",
            name="third_party",
            action=post_third_party,
            form=third_party_forms,
            strings=ThirdPartyForm,
            multiple=True
        )


class RemoveThirdParty(DeleteParty):
    def __init__(self, **kwargs):
        super().__init__(
            url="applications:third_parties",
            action=delete_third_party,
            error="Unexpected error removing third party user",
            multiple=True,
            **kwargs
        )
