from django.shortcuts import render
from django.urls import reverse_lazy

from core.models import Section, Tile


def hub(request):
    context = {
        'title': 'Exporter Hub',
        'sections': [
            Section("Get a licence", "placeholder", [
                Tile("Apply for a licence", "placeholder", reverse_lazy('new_application:index')),
            ]),
            Section("placeholder", "placeholder", [
                Tile("Drafts", "You have 4 drafts at the moment", reverse_lazy('drafts:drafts')),
                Tile("Applications", "placeholder", reverse_lazy('applications:applications')),
                Tile("Licences", "placeholder", reverse_lazy('licences:licences')),
            ]),
            Section("placeholder", "placeholder", [
                Tile("My Profile", "placeholder", "/placeholder"),
                Tile("Settings", "placeholder", "/placeholder"),
            ]),
            Section("placeholder", "placeholder", [
                Tile("Help", "Get help with all things LITE", "/placeholder"),
            ]),
        ],
    }
    return render(request, 'core/hub.html', context)


def signin(request):
    context = {
        'title': 'Sign in',
    }
    return render(request, 'core/signin.html', context)


def signout(request):
    context = {
        'title': 'Sign out',
    }
    return render(request, 'core/signout.html', context)


def placeholder(request):
    context = {
        'title': 'Placeholder',
    }
    return render(request, 'core/placeholder.html', context)
