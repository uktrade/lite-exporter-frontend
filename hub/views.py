from django.http import HttpResponse
from django.template import loader


def index(request):
    template = loader.get_template('hub/index.html')
    context = {
        'latest_question_list': "banana",
    }
    return HttpResponse(template.render(context, request))
