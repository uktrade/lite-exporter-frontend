from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from lite_forms.generators import error_page

from core.builtins.custom_tags import get_string
from core.services import get_units
from applications.services import get_draft_application, get_application_goods, get_application_goods_types, \
    post_draft_preexisting_goods, delete_application_preexisting_good
from goods.services import get_goods, get_good


class DraftGoodsList(TemplateView):
    def get(self, request, **kwargs):
        draft_id = str(kwargs['pk'])
        draft = get_draft_application(request, draft_id)
        goods = get_application_goods(request, draft_id)

        context = {
            'goods': goods,
            'draft': draft
        }
        return render(request, 'apply_for_a_licence/goods/index.html', context)


class GoodsList(TemplateView):
    def get(self, request, **kwargs):
        draft_id = str(kwargs['pk'])
        draft, _ = get_draft_application(request, draft_id)
        description = request.GET.get('description', '').strip()
        part_number = request.GET.get('part_number', '').strip()
        control_rating = request.GET.get('control_rating', '').strip()
        goods_list, _ = get_goods(request, {'description': description,
                                            'part_number': part_number,
                                            'control_rating': control_rating})

        filtered_data = []
        for good in goods_list:
            if good['documents'] and not good['is_good_controlled'] == 'unsure':
                filtered_data.append(good)

        context = {
            'title': get_string('goods.add_from_organisation.title'),
            'draft_id': draft_id,
            'data': filtered_data,
            'draft': draft,
            'description': description,
            'part_number': part_number,
            'control_code': control_rating
        }
        return render(request, 'apply_for_a_licence/goods/preexisting.html', context)


class DraftOpenGoodsList(TemplateView):
    def get(self, request, **kwargs):
        draft_id = str(kwargs['pk'])
        draft, _ = get_draft_application(request, draft_id)
        goods = get_application_goods(request, draft_id)

        context = {
            'title': 'Application Goods',
            'draft_id': draft_id,
            'goods': goods,
            'draft': draft
        }
        return render(request, 'apply_for_a_licence/goods/index.html', context)


class DraftOpenGoodsTypeList(TemplateView):
    def get(self, request, **kwargs):
        draft_id = str(kwargs['pk'])
        draft, _ = get_draft_application(request, draft_id)
        data, _ = get_application_goods_types(request, draft_id)

        context = {
            'title': get_string('good_types.overview_good_types.title'),
            'draft_id': draft_id,
            'data': data,
            'draft': draft
        }
        return render(request, 'apply_for_a_licence/goodstype/index.html', context)


class OpenGoodsList(TemplateView):
    def get(self, request, **kwargs):
        draft_id = str(kwargs['pk'])
        draft, _ = get_draft_application(request, draft_id)
        description = request.GET.get('description', '')
        data, _ = get_goods(request, {'description': description})

        context = {
            'title': 'Goods',
            'draft_id': draft_id,
            'data': data,
            'draft': draft,
            'description': description
        }
        return render(request, 'apply_for_a_licence/goods/preexisting.html', context)


class AddPreexistingGood(TemplateView):
    def get(self, request, **kwargs):
        good, _ = get_good(request, str(kwargs['good_pk']))

        context = {
            'title': 'Add a pre-existing good to your application',
            'page': goods.preexisting_good_form(good, get_units(request))
        }
        return render(request, 'form.html', context)

    def post(self, request, **kwargs):
        draft_id = str(kwargs['pk'])
        data, status_code = post_draft_preexisting_goods(request, draft_id, request.POST)

        if status_code != 201:
            good, status_code = get_good(request, str(kwargs['good_pk']))

            context = {
                'title': 'Add a pre-existing good to your application',
                'page': goods.preexisting_good_form(good, get_units(request)),
                'data': request.POST,
                'errors': data.get('errors'),
            }
            return render(request, 'form.html', context)

        return redirect(reverse_lazy('applications:goods', kwargs={'pk': draft_id}))


class RemovePreexistingGood(TemplateView):
    def get(self, request, **kwargs):
        application_id = str(kwargs['pk'])
        good_on_application_id = str(kwargs['good_on_application_pk'])

        status_code = delete_application_preexisting_good(request, good_on_application_id)

        if status_code != 204:
            return error_page(request, 'Unexpected error removing good')

        return redirect(reverse_lazy('applications:application_edit_overview', kwargs={'pk': application_id}))
