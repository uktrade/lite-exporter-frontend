import json

import requests
from django.shortcuts import render
from django.shortcuts import redirect
from formtools.wizard.views import NamedUrlSessionWizardView

from conf.settings import env


def index(request):
    context = {
        'title': 'Apply for a licence',
    }
    return render(request, 'new_application/index.html', context)


class ContactWizard(NamedUrlSessionWizardView):
    template_name = "new_application/page.html"

    def done(self, form_list, **kwargs):
        # do_something_with_the_form_data(form_list)
        return redirect('/new-application/draft/overview?id=123')


def overview(request):
    response = requests.get(env("LITE_API_URL") + '/drafts/' + request.GET.get('id'))
    data = json.loads(response.text)

    context = {
        'title': 'Overview',
        'data': data,
    }
    return render(request, 'new_application/overview.html', context)


def cancel(request):
    context = {
        'title': 'Are you sure you want to delete this application?',
        'draft_id': request.GET.get('id'),
    }
    return render(request, 'new_application/cancel_confirmation.html', context)


def cancel_confirm(request):
    requests.delete(env("LITE_API_URL") + '/drafts/' + request.GET.get('id'))

    context = {}
    return render(request, 'new_application/overview.html', context)
