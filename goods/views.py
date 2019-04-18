import requests
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from conf.settings import env
from goods import forms

GOODS_URL = env("LITE_API_URL") + '/goods/'


class Goods(TemplateView):
    def get(self, request, **kwargs):
        data = requests.get(GOODS_URL,
                            headers={'Authorization': 'Bearer ' + request.session['access_token']}).json()

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
        return render(request, 'form/form.html', context)

    def post(self, request, **kwargs):
        response = requests.post(GOODS_URL,
                                 json=request.POST,
                                 headers={'Authorization': 'Bearer ' + request.session['access_token']})

        if response.status_code == 400:
            context = {
                'title': 'Add Good',
                'page': forms.form,
                'data': request.POST,
                'errors': response.json().get('errors')
            }
            return render(request, 'form/form.html', context)

        return redirect('/goods/')
