from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from users import forms
from users.services import get_users, post_users


class Users(TemplateView):
    def get(self, request, **kwargs):
        data, status_code = get_users(request)

        context = {
          'data': data,
          'title': 'Manage Users',
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
