from django.shortcuts import render

from hub.models import Section, Tile


def index(request):
    context = {
        'title': 'Exporter Hub',
        'sections': [
            Section("Get a licence", "placeholder", [
                Tile("Apply for a licence", "placeholder", "/new-application")
            ]),
            Section("placeholder", "placeholder", [
                Tile("Drafts", "placeholder", "/drafts"),
                Tile("Applications", "placeholder", "/applications"),
                Tile("Licences", "placeholder", "/licences")
            ]),
            Section("placeholder", "placeholder", [
                Tile("My Profile", "placeholder", "/profile"),
                Tile("Settings", "placeholder", "/settings")
            ])
		],
    }
    return render(request, 'hub/index.html', context)
