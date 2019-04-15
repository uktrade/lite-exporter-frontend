import requests
from django.shortcuts import render
from django.views.generic import TemplateView

from conf.settings import env
from goods import forms



data = {
    'goods': [
        {
            'id': '123',
            'name': 'Moonshine Freeze',
            'description': 'Banana',
            'part_number': 'M123',
            'quantity': 123,
            'control_code': 'ML1a',
        },
        {
            'id': '123',
            'name': 'Moonshine Freeze',
            'description': 'Banana',
            'part_number': 'M123',
            'quantity': 123,
            'control_code': 'ML1a',
        },
        {
            'id': '123',
            'name': 'Moonshine Freeze',
            'description': 'Banana',
            'part_number': 'M123',
            'quantity': 123,
            'control_code': 'ML1a',
        },
        {
            'id': '123',
            'name': 'Moonshine Freeze',
            'description': 'Banana',
            'part_number': 'M123',
            'quantity': 123,
            'control_code': 'ML1a',
        }
    ],
}


class Goods(TemplateView):
    def get(self, request, **kwargs):
        # data = requests.get(env("LITE_API_URL") + '/goods/').json()

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
