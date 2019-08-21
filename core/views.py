from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from core.builtins.custom_tags import get_string
from core.forms import select_your_organisation_form
from core.helpers import Section, Tile, generate_notification_string
from core.services import get_notifications, get_clc_notifications, get_organisation
from libraries.forms.generators import form_page
from users.services import get_user


class Hub(TemplateView):
    def get(self, request, **kwargs):
        user, _ = get_user(request)
        response, _ = get_notifications(request, unviewed=True)
        num_notifications = response['count']
        response, _ = get_clc_notifications(request, unviewed=True)
        num_clc_notifications = response['count']
        organisation, _ = get_organisation(request, str(request.user.organisation))

        context = {
            'title': get_string('hub.title'),
            'organisation': organisation,
            'sections': [
                Section('', '', [
                    Tile(get_string('licences.apply_for_a_licence'), '',
                         reverse_lazy('apply_for_a_licence:index')),
                ]),
                Section('Manage', '', [
                    Tile(get_string('drafts.title'), '',
                         reverse_lazy('drafts:drafts')),
                    Tile(get_string('applications.title'), generate_notification_string(num_notifications),
                         reverse_lazy('applications:applications')),
                    Tile('Goods', generate_notification_string(num_clc_notifications),
                         reverse_lazy('goods:goods')),
                    Tile('Manage my organisation', '', reverse_lazy('users:users')),
                ]),
            ],
            'application_deleted': request.GET.get('application_deleted'),
            'user_data': user['user']
        }

        return render(request, 'core/hub.html', context)


class PickOrganisation(TemplateView):
    organisations = None

    def dispatch(self, request, *args, **kwargs):
        user, _ = get_user(request)
        self.organisations = user['user']['organisations']

        if len(self.organisations) == 1:
            raise Http404()

        return super(PickOrganisation, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        data = {
            'organisation': str(request.user.organisation)
        }

        return form_page(request, select_your_organisation_form(self.organisations), data=data)

    def post(self, request, **kwargs):
        request.user.organisation = request.POST['organisation']
        request.user.save()

        return redirect('/')
