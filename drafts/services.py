import requests

from conf.settings import env


def get_drafts(request):
    data = requests.get(env("LITE_API_URL") + '/drafts/', json={'id': str(request.user.id)})
    return data.json(), data.status_code
