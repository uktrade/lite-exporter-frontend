from django.views.generic import TemplateView
from lite_forms.generators import form_page

from applications.forms.reference_name import reference_name_form
from applications.services import get_application


class ApplicationEditReferenceName(TemplateView):
    def get(self, request, **kwargs):
        application_id = str(kwargs['pk'])
        get_application(request, application_id)

        return form_page(request, reference_name_form())
