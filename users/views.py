from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from core.form_components import Form, Question, InputType
from users import forms
from users.services import get_users, post_users, update_user, get_user


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


class ViewUser(TemplateView):
    def get(self, request, **kwargs):
        pk = request.GET.get('id')

        if pk is None:
            pk = str(request.user.id)

        data, status_code = get_user(request, pk)
        context = {
            'data': data,
            'title': 'User Profile'
        }
        return render(request, 'users/profile.html', context)


class EditUser(TemplateView):
    def get(self, request, **kwargs):
        data, status_code = get_user(request, request.GET.get('id'))
        context = {
            'data': data,
            'title': 'Edit User',
            'page': forms.edit_form,
        }
        return render(request, 'form/form.html', context)

    def post(self, request, **kwargs):
        data, status_code = update_user(request, request.GET.get('id'), request.POST)
        if status_code == 400:
            context = {
                'title': 'Add User',
                'page': forms.form,
                'data': request.POST,
                'errors': data.get('errors')
            }
            return render(request, 'form/form.html', context)

        return redirect('/users/profile/?id='+str(request.GET.get('id')))


def deactivate(request):
    context = {
        'title': 'Are you sure you want to deactivate this user?',
        'user_id': request.GET.get('id'),
    }
    return render(request, 'users/deactivate_confirmation.html', context)


def deactivate_confirm(request):
    update_user(request, request.GET.get('id'), json={"status": "deactivated"})

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
    update_user(request, request.GET.get('id'), json={"status": "active"})

    if request.GET.get('return') == 'users':
        return redirect('/users?user_reactivated=true')

    return redirect('/users?user_reactivated=true')
