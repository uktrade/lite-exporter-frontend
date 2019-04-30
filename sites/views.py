from django.shortcuts import render
from django.views.generic import TemplateView

from sites.services import get_sites


class Sites(TemplateView):
    def get(self, request, **kwargs):
        # data, status_code = get_sites(request)

        context = {
            'title': 'Sites',
            'data': {'sites': [
                {
                    'id': '123',
                    'name': 'SITE1',
                },
                {
                    'id': '123',
                    'name': 'SITE1',
                },
                {
                    'id': '123',
                    'name': 'SITE1',
                },
                {
                    'id': '123',
                    'name': 'SITE1',
                }
            ]},
        }
        return render(request, 'sites/index.html', context)
