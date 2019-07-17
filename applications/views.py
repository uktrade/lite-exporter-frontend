from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from applications.services import get_applications, get_application, post_application_notes


class ApplicationsList(TemplateView):
    def get(self, request, **kwargs):
        data, status_code = get_applications(request)

        if status_code is not 200:
            raise HttpResponse(status=status_code)

        context = {
            'data': data,
            'title': 'Applications',
        }
        return render(request, 'applications/index.html', context)


class ApplicationDetail(TemplateView):
    def get(self, request, **kwargs):
        application_id = str(kwargs['pk'])
        data, status_code = get_application(request, application_id)

        if status_code is not 200:
            return HttpResponse(status=status_code)

        context = {
            'data': data,
            'title': data.get('application').get('name'),
        }
        return render(request, 'applications/application.html', context)


class CaseNotes(TemplateView):
    def post(self, request, **kwargs):
        application_id = str(kwargs['pk'])
        data, status_code = get_application(request, application_id)
        case_id = data['application']['case']

        response, status_code = post_application_notes(request, case_id, request.POST)

        # if status_code is not 200:
        #     return HttpResponse(status=status_code)

        return redirect(reverse_lazy('applications:application', kwargs={'pk': application_id}))
