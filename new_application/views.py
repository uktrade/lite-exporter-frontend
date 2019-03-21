import json

import requests
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from conf.settings import env
from form import forms


def index(request):
    context = {
        'title': 'Apply for a licence',
    }
    return render(request, 'new_application/index.html', context)


def get_form_by_id(id):
    for form in forms.section1.forms:
        if form.id == id:
            return form
    return


def get_next_form_after_id(id):
    next_one = False
    for form in forms.section1.forms:
        if next_one:
            return form
        if form.id == id:
            next_one = True
    return


def start(request):
    return redirect("/new-application/form/" + str(forms.section1.forms[0].id))


def form(request, pk):
    if request.method == 'POST':
        data = {}

        # Add body fields to data
        for key, value in request.POST.items():
            if key != "button":
                data[key] = value

        # Set User ID
        data['user_id'] = '12345'

        # Post it to API
        if request.GET.get('id'):
            response = requests.put(env("LITE_API_URL") + '/drafts/' + request.GET.get('id') + '/',
                                    json=data)
            data = json.loads(response.text)
        else:
            response = requests.post(env("LITE_API_URL") + '/drafts/',
                                     json=data)
            data = json.loads(response.text)

        # If there are errors returned from LITE API, return and show them
        if 'errors' in data:
            page = get_form_by_id(pk)
            context = {
                'title': page.title,
                'page': page,
                'errors': data['errors'],
                'data': data,
                'draft_id': request.GET.get('id'),
            }
            return render(request, 'new_application/form.html', context)

        # Get the next form, if null go to overview
        next_form = get_next_form_after_id(pk)
        if next_form:
            return redirect(reverse_lazy('new_application:form',
                                         kwargs={'pk': next_form.id}) + '?id=' + str(data['draft']['id']))
        else:
            return redirect(reverse_lazy('new_application:overview') + '?id=' + request.GET.get('id'))

    elif request.method == 'GET':
        page = get_form_by_id(pk)
        data = {}

        if request.GET.get('id'):
            response = requests.get(env("LITE_API_URL") + '/drafts/' + request.GET.get('id'))
            data = json.loads(response.text)['draft']

        context = {
            'title': page.title,
            'page': page,
            'data': data,
            'draft_id': request.GET.get('id'),
        }
        return render(request, 'new_application/form.html', context)


def overview(request):
    response = requests.get(env("LITE_API_URL") + '/drafts/' + request.GET.get('id'))
    data = json.loads(response.text)

    context = {
        'title': 'Overview',
        'data': data,
    }
    return render(request, 'new_application/overview.html', context)


def cancel(request):
    context = {
        'title': 'Are you sure you want to delete this application?',
        'draft_id': request.GET.get('id'),
    }
    return render(request, 'new_application/cancel_confirmation.html', context)


def cancel_confirm(request):
    requests.delete(env("LITE_API_URL") + '/drafts/' + request.GET.get('id'))

    context = {}
    return render(request, 'new_application/overview.html', context)
