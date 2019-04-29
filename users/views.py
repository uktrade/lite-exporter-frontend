from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from users import forms
from users.services import get_users, post_users, deactivate_user, reactivate_user


class Users(TemplateView):
    def get(self, request, **kwargs):
        data, status_code = get_users(request)

        context = {
            'data': data,
            'title': 'Users',
            # 'userDeactivated': request.GET.get('user_deactivated')
        }
        return render(request, 'users/index.html', context)


class AddUser(TemplateView):
    def get(self, request, **kwargs):
        context = {
            'title': 'Add User',
            'page': forms.form,
        }
        return render(request, 'form/form.html', context)

    def post(self, request, **kwargs):
        data, status_code = post_users(request, request.POST)

        if status_code == 400:
            context = {
                'title': 'Add User',
                'page': forms.form,
                'data': request.POST,
                'errors': data.get('errors')
            }
            return render(request, 'form/form.html', context)

        return redirect('/users/')


def deactivate(request):
    context = {
        'title': 'Are you sure you want to deactivate this user?',
        'user_id': request.GET.get('id'),
    }
    return render(request, 'users/deactivate_confirmation.html', context)


def deactivate_confirm(request):
    deactivate_user(request, request.GET.get('id'), json={"status": "deactivated"})

    if request.GET.get('return') == 'users':
        return redirect('/users?user_deactivated=true')

    return redirect('/users/?user_deactivated=true')


def reactivate(request):
    context = {
        'title': 'Are you sure you want to reactivate this user?',
        'user_id': request.GET.get('id'),
    }
    return render(request, 'users/reactivate_confirmation.html', context)


def reactivate_confirm(request):
    reactivate_user(request, request.GET.get('id'), json={"status": "active"})

    if request.GET.get('return') == 'users':
        return redirect('/users?user_reactivated=true')

    return redirect('/users?user_reactivated=true')