import requests
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from conf.settings import env
from core.builtins.custom_tags import get_string
from core.helpers import Section, Tile


def hub(request):
    context = {
        'title': get_string('hub.title'),
        'sections': [
            Section("", "", [
                Tile(get_string('licences.apply_for_a_licence'), "", reverse_lazy('new_application:index')),
            ]),
            Section("Manage", "", [
                Tile(get_string('drafts.title'), "", reverse_lazy('drafts:drafts')),
                Tile(get_string('applications.title'), "", reverse_lazy('applications:applications')),
            ]),
        ],
        'applicationDeleted': request.GET.get('application_deleted'),
    }
    return render(request, 'core/hub.html', context)


def login(request):
    if request.method == 'GET':
        context = {
	        'title': get_string('misc.sign_in'),
        }
        return render(request, 'core/login.html', context)
    if request.method == 'POST':
        # Get token
        response = requests.post(env('LITE_API_URL') + '/o/token/',
                                 data={
                                     'grant_type': 'password',
                                     'username': request.POST.get('email'),
                                     'password': request.POST.get('password'),
                                     'client_id': env('CLIENT_ID'),
                                     'client_secret': env('CLIENT_SECRET'),
                                 },
                                 ).json()

        # If there are errors, return previous page
        if 'error' in response:
            context = {
		        'title': get_string('misc.sign_in'),
                'error': response.get('error'),
                'email': request.POST.get('email')
            }
            return render(request, 'core/login.html', context)

        access_token = response.get('access_token')

        header = {'Authorization': 'Bearer ' + access_token}

        user = requests.get(env('LITE_API_URL') + '/users/me/',
                            headers=header).json()

        # Set Session Info
        request.session['access_token'] = access_token
        request.session['user'] = user.get('user')

        # Redirect to index page as a signed in user
        return redirect('/')


def logout(request):
    context = {
        'title': get_string('misc.signed_out'),
    }
    request.session['access_token'] = None
    request.session['user'] = None
    return render(request, 'core/loggedout.html', context)
