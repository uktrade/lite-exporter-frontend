from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from applications.forms.parties import new_party_form_group
from applications.helpers.check_your_answers import convert_end_user
from applications.services import get_application, post_end_user, delete_end_user
from applications.views.parties.base import SetParty, DeleteParty, CopyExistingParty
from lite_content.lite_exporter_frontend.applications import EndUserForm


class EndUser(TemplateView):
    def get(self, request, **kwargs):
        application_id = str(kwargs["pk"])
        application = get_application(request, application_id)

        if application["end_user"]:
            context = {
                "application": application,
                "title": "End user",
                "edit_url": reverse_lazy("applications:set_end_user", kwargs={"pk": application_id}),
                "remove_url": reverse_lazy("applications:remove_end_user", kwargs={"pk": application_id}),
                "answers": convert_end_user(application["end_user"], application_id, True),
                "highlight": ["Document"] if not application["end_user"]["document"] else {},
            }
            return render(request, "applications/check-your-answer.html", context)
        else:
            return redirect(reverse_lazy("applications:set_end_user", kwargs={"pk": application_id}))


class SetEndUser(SetParty):
    def __init__(self):
        super().__init__(
            url="applications:end_user_attach_document",
            name="end_user",
            form=new_party_form_group,
            action=post_end_user,
            strings=EndUserForm,
            multiple=False,
        )


class RemoveEndUser(DeleteParty):
    def __init__(self):
        super().__init__(
            url="applications:set_end_user",
            action=delete_end_user,
            error="Unexpected error removing end user",
            multiple=False,
        )


class CopyExistingEndUser(CopyExistingParty):
    def __init__(self):
        super().__init__(
            destination_url="applications:set_end_user",
        )
