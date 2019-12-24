from django.shortcuts import render
from django.views.generic import TemplateView

from applications.services import get_additional_documents, get_application


class AdditionalDocuments(TemplateView):
    def get(self, request, **kwargs):
        application_id = str(kwargs["pk"])
        application = get_application(request, application_id)
        data = get_additional_documents(request, application_id)

        context = {"additional_documents": data["documents"], "application": application}

        return render(request, "applications/additional_documents/additional_documents.html", context)
