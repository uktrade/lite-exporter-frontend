from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from core.builtins.custom_tags import get_string
from drafts.services import get_draft, post_drafts, put_draft, delete_draft, submit_draft, get_draft_goods, get_drafts
from goods.services import get_goods
from new_application import forms


def index(request):
    context = {
        'title': get_string('licences.apply_for_a_licence'),
        'service_uses': get_string('licences.use_this_service_to'),
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
        data = request.POST

        # Send data to API
        if request.GET.get('id'):
            response, status_code = put_draft(request, request.GET.get('id'), data)
        else:
            response, status_code = post_drafts(request, data)

        # If there are errors returned from LITE API, return and show them
        if 'errors' in response:
            page = get_form_by_id(pk)
            context = {
                'title': page.title,
                'page': page,
                'errors': response['errors'],
                'data': data,
                'draft_id': request.GET.get('id'),
            }
            return render(request, 'form/form.html', context)

        # If a return query param is set, go there instead of the next form
        return_to = request.GET.get('return')

        if return_to == 'overview':
            return redirect(reverse_lazy('new_application:overview') + '?id=' + request.GET.get('id'))

        # Get the next form, if null go to overview
        next_form = get_next_form_after_id(pk)
        if next_form:
            return redirect(reverse_lazy('new_application:form',
                                         kwargs={'pk': next_form.id}) + '?id=' + str(response['draft']['id']))
        else:
            return redirect(reverse_lazy('new_application:overview') + '?id=' + request.GET.get('id'))

    elif request.method == 'GET':
        page = get_form_by_id(pk)
        data = {}

        if request.GET.get('id'):
            data, status_code = get_draft(request, request.GET.get('id'))
            data = data['draft']

        context = {
            'title': page.title,
            'page': page,
            'data': data,
            'draft_id': request.GET.get('id'),
        }
        return render(request, 'form/form.html', context)


def overview(request):
    draft_id = request.GET.get('id')
    data, status_code = get_draft(request, request.GET.get('id'))

    context = {
        'title': 'Overview',
        'data': data,
        'sections': [forms.section1],
        'draft_id': draft_id,
    }
    return render(request, 'new_application/overview.html', context)


def submit(request):
    data, status_code = submit_draft(request, request.GET.get('id'))

    if status_code is not 201:
        raise Http404

    context = {
        'title': 'Application Submitted',
        'data': data,
    }
    return render(request, 'new_application/application_success.html', context)


def cancel(request):
    context = {
        'title': 'Are you sure you want to delete this application?',
        'draft_id': request.GET.get('id'),
    }
    return render(request, 'new_application/cancel_confirmation.html', context)


def cancel_confirm(request):
    delete_draft(request, request.GET.get('id'))

    if request.GET.get('return') == 'drafts':
        return redirect('/drafts?application_deleted=true')

    return redirect('/?application_deleted=true')


def goods(request):
    draft_id = request.GET.get('id')
    data, status_code = get_draft_goods(request, draft_id)

    context = {
        'title': 'Goods',
        'draft_id': draft_id,
        'data': data,
    }
    return render(request, 'new_application/goods/index.html', context)


def add_preexisting(request):
    draft_id = request.GET.get('id')
    draft, status_code = get_draft(request, draft_id)
    data, status_code = get_goods(request)

    context = {
        'title': 'Goods',
        'draft_id': draft_id,
        'data': data,
        'draft': draft,
    }
    return render(request, 'new_application/goods/preexisting.html', context)