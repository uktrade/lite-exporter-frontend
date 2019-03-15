from django.shortcuts import render


def index(request):
    context = {
        'title': 'Exporter Hub',
    }
    return render(request, 'hub/index.html', context)
