from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from applications.forms.parties import new_party_form_group
from applications.helpers.check_your_answers import convert_consignee
from applications.services import get_application, post_consignee, delete_consignee
from applications.views.parties.base import SetParty, DeleteParty
from lite_content.lite_exporter_frontend.applications import ConsigneeForm


class Consignee(TemplateView):
    def get(self, request, **kwargs):
        application_id = str(kwargs["pk"])
        application = get_application(request, application_id)

        if application["consignee"]:
            context = {
                "application": application,
                "title": "Consignee",
                "edit_url": reverse_lazy("applications:set_consignee", kwargs={"pk": application_id}),
                "remove_url": reverse_lazy("applications:remove_consignee", kwargs={"pk": application_id}),
                "answers": convert_consignee(application["consignee"], application_id, True),
            }
            return render(request, "applications/check-your-answer.html", context)
        else:
            return redirect(reverse_lazy("applications:set_consignee", kwargs={"pk": application_id}))


class SetConsignee(SetParty):
    def __init__(self):
        super().__init__(
            url="applications:consignee_attach_document",
            name="consignee",
            form=new_party_form_group,
            action=post_consignee,
            strings=ConsigneeForm,
            multiple=False,
        )


class RemoveConsignee(DeleteParty):
    def __init__(self, **kwargs):
        super().__init__(
            url="applications:set_consignee",
            action=delete_consignee,
            error="Unexpected error removing consignee",
            multiple=False,
            **kwargs,
        )
