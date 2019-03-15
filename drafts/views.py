import json

import requests
from django.shortcuts import render

from conf.settings import env


def index(request):
    response = requests.get(env("LITE_API_URL") + '/drafts/')
    drafts = json.loads(response.text)

    context = {
        'title': 'Drafts',
        'drafts': drafts,
    }
    return render(request, 'drafts/index.html', context)
