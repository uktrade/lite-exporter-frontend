from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from goods import forms
from goods.services import get_goods, post_goods, get_good, update_good, delete_good


class Goods(TemplateView):
    def get(self, request, **kwargs):
        data, status_code = get_goods(request)

        context = {
          'data': data,
          'title': 'Manage Goods',
        }
        return render(request, 'goods/index.html', context)


class AddGood(TemplateView):
    def get(self, request, **kwargs):
        context = {
            'title': 'Add Good',
            'page': forms.form,
        }
        return render(request, 'form.html', context)

    def post(self, request, **kwargs):
        data, status_code = post_goods(request, request.POST)

        if status_code == 400:
            context = {
                'title': 'Add Good',
                'page': forms.form,
                'data': request.POST,
                'errors': data.get('errors')
            }
            return render(request, 'form.html', context)

        return redirect('/goods/')


class EditGood(TemplateView):

    def get(self, request, **kwargs):
        data, status_code = get_good(request, str(kwargs['pk']))
        context = {
            'title': 'Edit Good',
            'page': forms.edit_form,
            'data': data['good'],
        }
        return render(request, 'form.html', context)

    def post(self, request, **kwargs):
        data, status_code = update_good(request, str(kwargs['pk']),
                                        request.POST)

        if status_code == 400:
            context = {
                'title': 'Edit Good',
                'page': forms.edit_form,
                'data': request.POST,
                'errors': data.get('errors')
            }
            return render(request, 'form.html', context)
        return redirect('/goods/')


class DeleteGood(TemplateView):

    def get(self, request, **kwargs):
        data, status_code = get_good(request, str(kwargs['pk']))

        if data['good']['status'] != 'draft':
            context = {
                'title': 'Cannot Delete Good',
                'description': 'This good is already inside a application',
                'flag': 'cannot_delete',
            }
        else:
            context = {
                'good': data['good'],
                'title': 'Delete Good',
                'description': 'Are you sure you want to delete this good',
                'flag': 'can_delete',
            }
        return render(request, 'goods/confirm_delete.html', context)


class ConfirmDeleteGood(TemplateView):

    def get(self, request, **kwargs):
        print('im here')
        data, status_code = get_good(request, str(kwargs['pk']))
        if data['good']['status'] != 'draft':
            good_id = str(kwargs['pk'])
            print(good_id)
            delete_good(request, good_id)
            context = {
                'title': 'wayhay',
            }
           # return redirect('/goods/')
            return render(request, 'goods/index.html', context)
