from django.shortcuts import render


def index(request):
    context = {
        'latest_question_list': "banana",
    }
    return render(request, 'hub/index.html', context)
