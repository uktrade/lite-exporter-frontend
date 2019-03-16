import json

import requests
from django.shortcuts import render

from conf.settings import env


def index(request):
    response = requests.get(env("LITE_API_URL") + '/applications/')

    context = {
        'title': 'Applications',
        'applications': json.loads(response.text),
    }
    return render(request, 'applications/index.html', context)


def application(request, id):
    response = requests.get(env("LITE_API_URL") + '/applications/')

    context = {
        'title': 'Application for ML1a',
        'applications': json.loads(response.text),
    }
    return render(request, 'applications/application.html', context)
