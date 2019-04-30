from django.shortcuts import render
from django.views.generic import TemplateView

from sites import forms


class Sites(TemplateView):
    def get(self, request, **kwargs):
        # data, status_code = get_sites(request)

        context = {
            'title': 'Sites',
            'data': {'sites': [
                {
                    'id': '0fadea61-3ce1-4a31-abc3-4ad1ae677f3c',
                    'name': 'SITE1',
                },
                {
                    'id': '0fadea61-3ce1-4a31-abc3-4ad1ae677f3c',
                    'name': 'SITE1',
                },
                {
                    'id': '0fadea61-3ce1-4a31-abc3-4ad1ae677f3c',
                    'name': 'SITE1',
                },
                {
                    'id': '0fadea61-3ce1-4a31-abc3-4ad1ae677f3c',
                    'name': 'SITE1',
                }
            ]},
        }
        return render(request, 'sites/index.html', context)


class NewSite(TemplateView):
    def get(self, request, **kwargs):
        context = {
            'title': 'New Site',
            'page': forms.new_site_form
        }
        return render(request, 'form/form.html', context)


class EditSite(TemplateView):
    def get(self, request, **kwargs):
        # data, status_code = get_site(request, pk)

        context = {
            'title': 'Edit Site',
            'page': forms.edit_site_form
        }
        return render(request, 'form/form.html', context)
