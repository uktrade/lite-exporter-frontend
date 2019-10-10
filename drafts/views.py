from django.shortcuts import render
from django.views.generic import TemplateView

from drafts.services import get_drafts


class DraftsList(TemplateView):
    def get(self, request, **kwargs):
        data, status_code = get_drafts(request)

        context = {
            'title': 'Applications',
            'data': data
        }
        return render(request, 'applications/drafts.html', context)
