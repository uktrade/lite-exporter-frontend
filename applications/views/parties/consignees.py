from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from applications.forms.parties import new_party_form_group
from applications.helpers.check_your_answers import convert_consignee
from applications.services import get_application, post_party, delete_party, validate_party
from applications.views.parties.base import AddParty, ExistingPartiesList, SetParty, DeleteParty
from lite_content.lite_exporter_frontend.applications import ConsigneeForm, ConsigneePage


class Consignee(TemplateView):
    def get(self, request, **kwargs):
        application_id = str(kwargs["pk"])
        application = get_application(request, application_id)

        if application["consignee"]:
            kwargs = {"pk": application_id, "obj_pk": application["consignee"]["id"]}
            context = {
                "application": application,
                "title": ConsigneePage.TITLE,
                "edit_url": reverse_lazy("applications:edit_consignee", kwargs=kwargs),
                "remove_url": reverse_lazy("applications:remove_consignee", kwargs=kwargs),
                "answers": convert_consignee(application["consignee"], application_id, application["is_major_editable"]),
            }
            return render(request, "applications/check-your-answer.html", context)
        else:
            return redirect(reverse_lazy("applications:add_consignee", kwargs={"pk": application_id}))


class AddConsignee(AddParty):
    def __init__(self):
        super().__init__(
            new_url="applications:set_consignee", copy_url="applications:copy_consignee", party_type="consignee",
        )


class SetConsignee(SetParty):
    def __init__(self, copy_existing=False):
        super().__init__(
            url="applications:consignee_attach_document",
            party_type="consignee",
            form=new_party_form_group,
            back_url="applications:add_consignee",
            strings=ConsigneeForm,
            multiple_allowed=True,
            copy_existing=copy_existing,
            post_action=post_party,
            validate_action=validate_party,
        )


class EditConsignee(SetConsignee):
    def __init__(self):
        super().__init__(copy_existing=True)


class RemoveConsignee(DeleteParty):
    def __init__(self, **kwargs):
        super().__init__(
            url="applications:add_consignee",
            action=delete_party,
            error=ConsigneePage.DELETE_ERROR,
            multiple_allowed=True,
            **kwargs,
        )


class ExistingConsignee(ExistingPartiesList):
    def __init__(self):
        super().__init__(destination_url="applications:set_consignee", back_url="applications:add_consignee")
