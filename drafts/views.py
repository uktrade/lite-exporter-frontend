import libraries.jsondate as json

import requests
from django.shortcuts import render

from conf.settings import env


def index(request):
    response = requests.get(env("LITE_API_URL") + '/drafts/')

    context = {
        'title': 'Drafts',
        'data': json.loads(response.text),
    }
    return render(request, 'drafts/index.html', context)
