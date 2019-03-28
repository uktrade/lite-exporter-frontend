from django.shortcuts import render
from django.urls import reverse_lazy

from core.helpers import Section, Tile


def hub(request):
    context = {
        'title': 'Exporter Hub',
        'sections': [
            Section("", "", [
                Tile("Apply for a licence", "", reverse_lazy('new_application:index')),
            ]),
            Section("Manage", "", [
                Tile("Drafts", "", reverse_lazy('drafts:drafts')),
                Tile("Applications", "", reverse_lazy('applications:applications')),
            ]),
        ],
        'applicationDeleted': request.GET.get('application_deleted')
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
