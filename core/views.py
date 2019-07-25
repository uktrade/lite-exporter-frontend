from django.shortcuts import render
from django.urls import reverse_lazy

from core.builtins.custom_tags import get_string
from core.helpers import Section, Tile
from core.services import get_notifications, get_clc_notifications


def hub(request):
    response, _ = get_notifications(request, unviewed=True)
    if response['count'] > 0:
        num_notifications = response['count']
    else:
        num_notifications = ''
    response, _ = get_clc_notifications(request, unviewed=True)
    if response['count'] > 0:
        num_clc_notifications = response['count']
    else:
        num_clc_notifications = ''

    context = {
        'title': get_string('hub.title'),
        'sections': [
            Section('', '', [
                Tile(get_string('licences.apply_for_a_licence'), '',
                     reverse_lazy('apply_for_a_licence:index')),
            ]),
            Section('Manage', '', [
                Tile(get_string('drafts.title'), '',
                     reverse_lazy('drafts:drafts')),
                Tile(get_string('applications.title'), num_notifications,
                     reverse_lazy('applications:applications')),
                Tile('Goods', num_clc_notifications,
                     reverse_lazy('goods:goods')),
                Tile('Sites', '', reverse_lazy('sites:sites')),
                Tile('Users', '', reverse_lazy('users:users')),
            ]),
        ],
        'applicationDeleted': request.GET.get('application_deleted'),
    }
    return render(request, 'core/hub.html', context)
