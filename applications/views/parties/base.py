from http import HTTPStatus

from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from applications.services import get_application, get_existing_parties
from core.helpers import convert_parameters_to_query_params
from lite_forms.generators import error_page
from lite_forms.views import MultiFormView


class SetParty(MultiFormView):
    def __init__(self, url, form, name, action, strings, multiple, **kwargs):
        super().__init__(**kwargs)
        self.url = url
        self.name = name
        self.action = action
        self.strings = strings
        self.form = form
        self.multiple = multiple

    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        application = get_application(request, self.object_pk)
        self.forms = self.form(application, self.strings)
        if self.multiple:
            self.data = None
        else:
            self.data = application[self.name]

    def get_success_url(self):
        if self.multiple:
            return reverse_lazy(
                self.url, kwargs={"pk": self.object_pk, "obj_pk": self.get_validated_data()[self.name]["id"]}
            )
        else:
            return reverse_lazy(self.url, kwargs={"pk": self.object_pk})


class DeleteParty(TemplateView):
    def __init__(self, url, action, error, multiple, **kwargs):
        super().__init__(**kwargs)
        self.url = url
        self.action = action
        self.error = error
        self.multiple = multiple

    def get(self, request, **kwargs):
        application_id = str(kwargs["pk"])
        if self.multiple:
            status_code = self.action(request, application_id, str(kwargs["obj_pk"]))
        else:
            status_code = self.action(request, application_id)

        if status_code != HTTPStatus.NO_CONTENT:
            return error_page(request, self.error)

        return redirect(reverse_lazy(self.url, kwargs={"pk": application_id}))


class CopyExistingParty(TemplateView):
    def __int__(self, destination_url, **kwargs):
        super().__init__(**kwargs)
        self.destination_url = destination_url

    def get(self, request, **kwargs):
        """
        List of existing parties
        """
        application_id = str(kwargs["pk"])
        params = convert_parameters_to_query_params(request.GET)
        parties, _ = get_existing_parties(request, application_id, params)

        context = {
            "title": "Existing Parties",
            "draft_id": application_id,
            "data": parties,
            "url": self.destination_url,
        }
        return render(request, "applications/parties/preexisting.html", context)
