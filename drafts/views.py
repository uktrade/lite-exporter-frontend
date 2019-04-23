import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from conf.settings import env


@login_required
def index(request):
    response = requests.get(env("LITE_API_URL") + '/drafts/', json={'id': str(request.user.id)})

    context = {
        'title': 'Drafts',
        'data': response.json(),
        'applicationDeleted': request.GET.get('application_deleted')
    }
    return render(request, 'drafts/index.html', context)
