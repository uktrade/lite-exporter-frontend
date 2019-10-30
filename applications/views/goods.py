from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from lite_forms.components import HiddenField, Button
from lite_forms.generators import error_page
from s3chunkuploader.file_handler import S3FileUploadHandler
from django.utils.decorators import method_decorator

from applications.forms.goods import good_on_application_form, add_new_good_forms
from applications.services import get_application, get_application_goods, get_application_goods_types, \
    post_application_preexisting_goods, delete_application_preexisting_good, validate_application_good, \
    add_document_data
from core.services import get_units
from goods.services import get_goods, get_good, validate_good, post_good, post_good_documents


class DraftGoodsList(TemplateView):
    def get(self, request, **kwargs):
        """
        List all goods related to the draft
        """
        draft_id = str(kwargs['pk'])
        application = get_application(request, draft_id)
        goods = get_application_goods(request, draft_id)

        context = {
            'goods': goods,
            'application': application
        }
        return render(request, 'applications/goods/index.html', context)


class GoodsList(TemplateView):
    def get(self, request, **kwargs):
        """
        List of existing goods  (add-preexisting)
        """
        application_id = str(kwargs['pk'])
        application = get_application(request, application_id)
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
            'application': application,
            'data': filtered_data,
            'description': description,
            'part_number': part_number,
            'control_code': control_rating,
            'draft_id': application_id
        }
        return render(request, 'applications/goods/preexisting.html', context)


@method_decorator(csrf_exempt, 'dispatch')
class AddNewGood(TemplateView):
    def get(self, request, **kwargs):
        form = add_new_good_forms(request)[0]
        form.questions.append(HiddenField('form_name', value='good_details'))
        form.buttons = [Button('Continue', 'continue')]
        context = {
            'page': form
        }
        return render(request, 'form.html', context)

    @csrf_exempt
    def post(self, request, **kwargs):
        # This has to be run at the top of the method before POST is accessed.
        self.request.upload_handlers.insert(0, S3FileUploadHandler(request))

        application_id = str(kwargs['pk'])
        form_name = request.POST.get('form_name')
        context = {}
        post = {}
        good_details_form_fields = ['description', 'control_code', 'part_number', 'is_good_controlled',
                                    'is_good_end_product']
        good_on_application_form_fields = ['value', 'quantity', 'unit']

        if form_name == 'good_details':
            for field in good_details_form_fields:
                post[field] = request.POST.get(field, None)

            data = validate_good(request, post)

            if data.status_code != 200:
                form = add_new_good_forms(request)[0]
                form.questions.append(HiddenField('form_name', value='good_details'))
                form.buttons = [Button('Continue', 'continue')]
                context['errors'] = data.json()['errors']
                context['data'] = post
            else:
                form = add_new_good_forms(request)[1]
                form.questions.append(HiddenField('form_name', value='good_on_application_details'))
                for field in good_details_form_fields:
                    form.questions.append(HiddenField(('good_' + field), value=post[field]))
                form.buttons = [Button('Continue', 'continue')]

        elif form_name == 'good_on_application_details':
            for field in good_on_application_form_fields:
                post[field] = request.POST.get(field, None)

            data = validate_application_good(request, application_id, post)

            if data.status_code != 200:
                form = add_new_good_forms(request)[1]
                form.questions.append(HiddenField('form_name', value='good_on_application_details'))
                form.buttons = [Button('Continue', 'continue')]

                for field in good_details_form_fields:
                    field_name = 'good_' + field
                    value = request.POST.get(field_name, None)
                    form.questions.append(HiddenField(field_name, value=value))

                context['errors'] = data.json()['errors']
                context['data'] = post
            else:
                form = add_new_good_forms(request)[2]
                form.questions.append(HiddenField('form_name', value='good_document'))

                for field in good_details_form_fields:
                    field_name = 'good_' + field
                    value = request.POST.get(field_name, None)
                    form.questions.append(HiddenField(field_name, value=value))

                for field in good_on_application_form_fields:
                    field_name = 'good_on_app_' + field
                    form.questions.append(HiddenField(field_name, value=post[field]))

        elif form_name == 'good_document':
            if request.FILES:
                # post goods
                for field in good_details_form_fields:
                    post[field] = request.POST.get(('good_' + field), None)

                validated_data, status_code = post_good(request, post)

                if status_code != 201:
                    raise Http404

                # attach document
                good_id = validated_data['good']['id']
                good, _ = get_good(request, good_id)
                data, error = add_document_data(request)

                if error:
                    return error_page(None, error)

                if 'description' not in data:
                    data['description'] = ''
                data = [data]
                # Send LITE API the file information
                good_documents, _ = post_good_documents(request, good_id, data)

                # Attach good to application
                post = {'good_id': good_id}
                for field in good_on_application_form_fields:
                    post[field] = request.POST.get(('good_on_app_' + field), None)

                _, _ = post_application_preexisting_goods(request, application_id, post)

                # make all 3 post requests.
                return redirect('applications:goods', application_id)
            else:
                for field in (good_on_application_form_fields + good_on_application_form_fields):
                    post[field] = request.POST.get(field, None)

                form = add_new_good_forms(request)[2]
                form.questions.append(HiddenField('form_name', value='good_document'))
                context['errors'] = {'': ['A document is required.']}

        context['page'] = form

        return render(request, 'form.html', context)


class DraftOpenGoodsTypeList(TemplateView):
    def get(self, request, **kwargs):
        application_id = str(kwargs['pk'])
        application = get_application(request, application_id)
        goods = get_application_goods_types(request, application_id)

        context = {
            'goods': goods,
            'application': application,
        }
        return render(request, 'applications/goodstype/index.html', context)


class AddPreexistingGood(TemplateView):
    def get(self, request, **kwargs):
        good, _ = get_good(request, str(kwargs['good_pk']))

        context = {
            'title': 'Add a pre-existing good to your application',
            'page': good_on_application_form(good, get_units(request))
        }
        return render(request, 'form.html', context)

    def post(self, request, **kwargs):
        draft_id = str(kwargs['pk'])
        data, status_code = post_application_preexisting_goods(request, draft_id, request.POST)

        if status_code != 201:
            good, status_code = get_good(request, str(kwargs['good_pk']))

            context = {
                'title': 'Add a pre-existing good to your application',
                'page': good_on_application_form(good, get_units(request)),
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

        if status_code != 200:
            return error_page(request, 'Unexpected error removing good')

        return redirect(reverse_lazy('applications:goods', kwargs={'pk': application_id}))
