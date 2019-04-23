from conf.client import get


def get_drafts(request):
    data = get(request, '/drafts/')
    return data.json(), data.status_code


def get_draft(request, pk):
    data = get(request, '/drafts/' + pk)
    return data.json(), data.status_code
