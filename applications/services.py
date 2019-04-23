import requests

from conf.settings import env


def get_applications(request):
    data = requests.get(env("LITE_API_URL") + '/applications/', json={'id': str(request.user.id)})
    return data.json(), data.status_code


def get_application(request, pk):
    data = requests.get(env("LITE_API_URL") + '/applications/' + pk, json={'id': str(request.user.id)})
    return data.json(), data.status_code
