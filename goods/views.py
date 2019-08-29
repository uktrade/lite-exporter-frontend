from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from lite_forms.generators import error_page, form_page
from s3chunkuploader.file_handler import S3FileUploadHandler

from core.services import get_clc_notifications
from goods import forms
from goods.forms import edit_form, attach_documents_form
from goods.services import get_goods, post_goods, get_good, update_good, delete_good, get_good_documents, \
    get_good_document, delete_good_document, post_good_documents, raise_clc_query
from apply_for_a_licence.services import add_document_data
from apply_for_a_licence.services import download_document_from_s3


class Goods(TemplateView):
    def get(self, request, **kwargs):
        data, status_code = get_goods(request)
        notifications, _ = get_clc_notifications(request, unviewed=True)
        notifications_ids_list = [x['clc_query'] for x in notifications['results']]

        context = {
            'data': data,
            'title': 'Manage Goods',
            'notifications_ids_list': notifications_ids_list,
        }
        return render(request, 'goods/index.html', context)


class GoodsDetail(TemplateView):
    def get(self, request, **kwargs):
        good_id = kwargs['pk']
        data, status_code = get_good(request, str(good_id))
        documents, status_code = get_good_documents(request, str(good_id))

        if data['good'].get('clc_query_id') != 'None':
            if data['good']['notes'] is not None:
                visible_notes = filter(lambda note: note['is_visible_to_exporter'], data['good']['notes'])

                context = {
                    'data': data,
                    'documents': documents['documents'],
                    'notes': visible_notes,
                    'title': data['good']['description'],
                }

                return render(request, 'goods/good.html', context)

        context = {
            'data': data,
            'documents': documents['documents'],
            'title': data['good']['description'],
        }
        return render(request, 'goods/good.html', context)


class AddGood(TemplateView):
    main_form = forms.add_goods_questions

    def get(self, request, **kwargs):
        return form_page(request, self.main_form)

    def post(self, request):
        data = request.POST.copy()
        data['validate_only'] = False

        validated_data, status_code = post_goods(request, data)

        if 'errors' in validated_data:
            if validated_data['errors']:
                return form_page(request, self.main_form, data=data, errors=validated_data.get('errors'))

        return redirect(reverse_lazy('goods:attach_documents', kwargs={'pk': validated_data['good']['id']}))


class RaiseCLCQuery(TemplateView):
    def get(self, request, **kwargs):
        return form_page(request, forms.are_you_sure(str(kwargs['pk'])))

    def post(self, request, **kwargs):
        good_id = str(kwargs['pk'])
        request_data = request.POST.copy()
        request_data['good_id'] = good_id

        data, status_code = raise_clc_query(request, request_data)
        if 'errors' in data:
            return form_page(request, forms.are_you_sure(str(kwargs['pk'])), data=request_data, errors=data['errors'])

        return redirect(reverse('goods:goods'))


class DraftAddGood(TemplateView):
    def get(self, request, **kwargs):
        return form_page(request, forms.form)

    def post(self, request, **kwargs):
        data, status_code = post_goods(request, request.POST)

        if status_code == 400:
            return form_page(request, forms.form, request.POST, errors=data['errors'])

        return redirect(reverse_lazy('apply_for_a_licence:overview'), kwargs['pk'])


class EditGood(TemplateView):
    def get(self, request, **kwargs):
        data, status_code = get_good(request, str(kwargs['pk']))
        return form_page(request, edit_form, data['good'])

    def post(self, request, **kwargs):
        data, status_code = update_good(request, str(kwargs['pk']), request.POST)

        if status_code == 400:
            return form_page(request, edit_form, request.POST, errors=data['errors'])

        return redirect(reverse_lazy('goods:goods'))


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
                'description': 'Are you sure you want to delete this good?',
                'flag': 'can_delete',
            }
        return render(request, 'goods/confirm_delete.html', context)

    def post(self, request, **kwargs):
        delete_good(request, str(kwargs['pk']))
        return redirect(reverse_lazy('goods:goods'))


@method_decorator(csrf_exempt, 'dispatch')
class AttachDocuments(TemplateView):
    def get(self, request, **kwargs):
        good_id = str(kwargs['pk'])
        get_good(request, good_id)

        form = attach_documents_form(reverse('goods:good', kwargs={'pk': good_id}))

        return form_page(request, form, extra_data={'good_id': good_id})

    @csrf_exempt
    def post(self, request, **kwargs):
        self.request.upload_handlers.insert(0, S3FileUploadHandler(request))

        good_id = str(kwargs['pk'])
        good, status_code = get_good(request, good_id)

        data, error = add_document_data(request)
        if 'description' not in data:
            data['description'] = ''
        data = [data]

        if error:
            return error_page(None, error)

        # Send LITE API the file information
        good_documents, status_code = post_good_documents(request, good_id, data)

        if 'errors' in good_documents:
            return error_page(None, 'We had an issue uploading your files. Try again later.')

        if good['good']['is_good_controlled'] == 'unsure':
            return redirect(reverse('goods:raise_clc_query', kwargs={'pk': good_id}))

        return redirect(reverse('goods:good', kwargs={'pk': good_id}))


class Document(TemplateView):
    def get(self, request, **kwargs):
        good_id = str(kwargs['pk'])
        file_pk = str(kwargs['file_pk'])

        get_good(request, good_id)
        document, status_code = get_good_document(request, good_id, file_pk)
        return download_document_from_s3(document['document']['s3_key'], document['document']['name'])


class DeleteDocument(TemplateView):
    def get(self, request, **kwargs):
        good_id = str(kwargs['pk'])
        file_pk = str(kwargs['file_pk'])

        good, status_code = get_good(request, good_id)
        document, status_code = get_good_document(request, good_id, file_pk)
        original_file_name = document['document']['name']

        context = {
            'title': 'Are you sure you want to delete this file?',
            'description': original_file_name,
            'good': good['good'],
            'document': document['document'],
            'page': 'goods/modals/delete_document.html',
        }
        return render(request, 'core/static.html', context)

    def post(self, request, **kwargs):
        good_id = str(kwargs['pk'])
        file_pk = str(kwargs['file_pk'])

        good, status_code = get_good(request, good_id)
        document, status_code = get_good_document(request, good_id, file_pk)
        # Delete the file on the API
        delete_good_document(request, good_id, file_pk)

        context = {
            'title': 'Are you sure you want to delete this file?',
            'description': document['document']['name'],
            'good': good['good'],
            'document': document['document'],
            'page': 'goods/modals/delete_document.html',
        }
        return redirect(reverse('goods:good', kwargs={'pk': good_id}))
