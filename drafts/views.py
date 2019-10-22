from django.shortcuts import render
from django.views.generic import TemplateView

from drafts.services import get_draft_applications


class DraftsList(TemplateView):
    def get(self, request, **kwargs):
        data = get_draft_applications(request)

        context = {
            'title': 'Applications',
            'data': data
        }
        return render(request, 'applications/drafts.html', context)
