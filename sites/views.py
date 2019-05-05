from django.shortcuts import render
from django.views.generic import TemplateView

from sites import forms
from sites.services import get_sites, get_site


class Sites(TemplateView):
    def get(self, request, **kwargs):
        data, status_code = get_sites(request)

        context = {
            'title': 'Sites',
            'data': data,
        }
        return render(request, 'sites/index.html', context)


class NewSite(TemplateView):
    def get(self, request, **kwargs):
        context = {
            'title': 'New Site',
            'page': forms.new_site_form,
        }
        return render(request, 'form.html', context)


class EditSite(TemplateView):
    def get(self, request, **kwargs):
        data, status_code = get_site(request, kwargs['pk'])

        context = {
            'title': 'Edit Site',
            'page': forms.edit_site_form,
        }
        return render(request, 'form.html', context)
