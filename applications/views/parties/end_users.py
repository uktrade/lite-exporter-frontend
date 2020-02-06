from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from applications.forms.parties import new_party_form_group
from applications.helpers.check_your_answers import convert_party
from applications.services import get_application, post_party, validate_party, delete_party
from applications.views.parties.base import AddParty, SetParty, DeleteParty, ExistingPartiesList
from lite_content.lite_exporter_frontend.applications import EndUserForm, EndUserPage


class EndUser(TemplateView):
    def get(self, request, **kwargs):
        application_id = str(kwargs["pk"])
        application = get_application(request, application_id)
        if application["end_user"]:
            kwargs = {"pk": application_id, "obj_pk": application["end_user"]["id"]}
            context = {
                "application": application,
                "title": EndUserPage.TITLE,
                "edit_url": reverse_lazy("applications:edit_end_user", kwargs=kwargs),
                "remove_url": reverse_lazy("applications:remove_end_user", kwargs=kwargs),
                "answers": convert_party(application["end_user"], application_id, application["is_major_editable"]),
                "highlight": ["Document"] if not application["end_user"]["document"] else {},
            }

            return render(request, "applications/check-your-answer.html", context)
        else:
            return redirect(reverse_lazy("applications:add_end_user", kwargs={"pk": application_id}))


class AddEndUser(AddParty):
    def __init__(self):
        super().__init__(
            new_url="applications:set_end_user", copy_url="applications:copy_end_user", party_type="end_user",
        )


class SetEndUser(SetParty):
    def __init__(self, copy_existing=False):
        super().__init__(
            url="applications:end_user_attach_document",
            party_type="end_user",
            form=new_party_form_group,
            back_url="applications:add_end_user",
            strings=EndUserForm,
            multiple_allowed=True,
            copy_existing=copy_existing,
            post_action=post_party,
            validate_action=validate_party,
        )


class EditEndUser(SetEndUser):
    def __init__(self):
        super().__init__(copy_existing=True)


class RemoveEndUser(DeleteParty):
    def __init__(self):
        super().__init__(
            url="applications:add_end_user", action=delete_party, error=EndUserPage.DELETE_ERROR, multiple_allowed=True,
        )


class ExistingEndUser(ExistingPartiesList):
    def __init__(self):
        super().__init__(destination_url="applications:set_end_user", back_url="applications:add_end_user")
