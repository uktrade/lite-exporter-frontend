from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from lite_forms.generators import form_page

from drafts.services import get_draft_goods_type, get_draft_countries
from goodstype import forms
from goodstype.services import post_goods_type, get_goods_type, post_goods_type_countries


class GoodsType(TemplateView):
    def get(self, request, pk):
        data, _ = get_goods_type(request, pk)

        context = {
            'data': data,
            'title': 'Manage GoodsTypes',
        }
        return render(request, 'goodstype/index.html', context)


class AddGoodsType(TemplateView):
    def get(self, request, **kwargs):
        return form_page(request, forms.form)

    def post(self, request, **kwargs):
        copied_post = request.POST.copy()
        copied_post['content_type'] = 'draft'
        copied_post['object_id'] = kwargs.get('pk')
        data, status_code = post_goods_type(request, copied_post)

        if status_code == 400:
            return form_page(request, forms.form, request.POST, errors=data['errors'])

        return redirect(reverse_lazy('goods:goods'))


class DraftAddGoodsType(TemplateView):
    def get(self, request, **kwargs):
        return form_page(request, forms.form)

    def post(self, request, **kwargs):
        copied_post = request.POST.copy()
        copied_post['content_type'] = 'draft'
        copied_post['object_id'] = str(kwargs.get('pk'))
        data, status_code = post_goods_type(request, copied_post)

        if status_code == 400:
            return form_page(request, forms.form, request.POST, errors=data['errors'])

        next = request.GET.get('next')
        if next:
            return redirect(next)
        return redirect(reverse_lazy('apply_for_a_licence:overview', args=[kwargs['pk']]))


class GoodsTypeCountries(TemplateView):
    def get(self, request, *args, **kwargs):
        goods, _ = get_draft_goods_type(request, str(kwargs['pk']))
        countries, _ = get_draft_countries(request, str(kwargs['pk']))

        context = {
            'countries': countries,
            'goods': goods,
            'description': "hello"
        }
        return render(request, 'apply_for_a_licence/goodstype/countries.html', context)

    def post(self, request, **kwargs):
        data = request.POST.copy()

        goods, _ = get_draft_goods_type(request, str(kwargs['pk']))
        post_data = {}

        for country in data:
            split_data = country.split('.')
            if str(split_data[0]) not in str(post_data):
                post_data[split_data[0]] = []
            post_data[split_data[0]].append(split_data[-1])

        post_goods_type_countries(request, post_data)

        countries, _ = get_draft_countries(request, str(kwargs['pk']))

        context = {
            'countries': countries,
            'goods': goods,
            'description': "hello"
        }

        return render(request, 'apply_for_a_licence/goodstype/countries.html', context)

