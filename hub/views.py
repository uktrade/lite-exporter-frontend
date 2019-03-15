from django.shortcuts import render
from django.urls import reverse_lazy

from hub.models import Section, Tile


def index(request):
    context = {
        'title': 'Exporter Hub',
        'sections': [
            Section("Get a licence", "placeholder", [
                Tile("Apply for a licence", "placeholder", reverse_lazy('new_application:index')),
            ]),
            Section("placeholder", "placeholder", [
                Tile("Drafts", "You have 4 drafts at the moment", reverse_lazy('drafts:drafts')),
                Tile("Applications", "placeholder", "/applications"),
                Tile("Licences", "placeholder", "/licences"),
            ]),
            Section("placeholder", "placeholder", [
                Tile("My Profile", "placeholder", "/profile"),
                Tile("Settings", "placeholder", "/settings"),
            ]),
            Section("placeholder", "placeholder", [
                Tile("Help", "Get help with all things LITE", "/help"),
            ]),
        ],
    }
    return render(request, 'hub/index.html', context)
