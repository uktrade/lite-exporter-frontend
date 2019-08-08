from django.http import StreamingHttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from s3chunkuploader.file_handler import S3FileUploadHandler, s3_client

from conf import settings
from conf.settings import AWS_STORAGE_BUCKET_NAME
from core.builtins.custom_tags import get_string
from core.services import get_clc_notifications
from goods import forms
from goods.forms import edit_form, attach_documents_form
from goods.services import get_goods, post_goods, get_good, update_good, delete_good, get_good_documents, get_good_document, delete_good_document, post_good_documents
from libraries.forms.components import HiddenField
from libraries.forms.generators import form_page, error_page


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

        # visible_notes = filter(lambda note: note['is_visible_to_exporter'], data['good']['notes'])

        context = {
            'data': data,
            'documents': documents['documents'],
            # 'notes': visible_notes,
            'title': data['good']['description'],
        }

        return render(request, 'goods/good.html', context)


class AddGood(TemplateView):
    main_form = forms.add_goods_questions

    def get(self, request, **kwargs):
        return form_page(request, self.main_form)

    def post(self, request):
        data = request.POST.copy()

        # Logic for when we are at the confirmation page
        data['validate_only'] = False

        if 'clc_query_confirmation' in data:
            if data['is_good_controlled'] == 'unsure' and data['clc_query_confirmation'] == 'yes':
                data['are_you_sure'] = True
                data['control_code'] = data['not_sure_details_control_code']
                data, status_code = post_goods(request, data)
                if status_code == 400:
                    return form_page(request, self.main_form, request.POST, errors=data['errors'])

                return redirect(reverse_lazy('goods:goods'))
            elif data['is_good_controlled'] == 'unsure' and data['clc_query_confirmation'] == 'no':
                # user answered no on confirmation page and return to goods list
                return redirect(reverse_lazy('goods:goods'))

        # On first page - validate without saving to see if we should head for confirmation page
        data['validate_only'] = True
        validated_data, status_code = post_goods(request, data)

        if 'errors' in validated_data and validated_data['errors']:
            return form_page(request, self.main_form, data=data, errors=validated_data.get('errors'))

        data['validate_only'] = False

        # on first page for unsure good and no errors - put all data from first form in hidden fields and direct to
        # confirmation page
        if 'is_good_controlled' in data and data['is_good_controlled'] == 'unsure':
            are_you_sure_form = forms.are_you_sure
            for key, value in data.items():
                are_you_sure_form.questions.append(
                    HiddenField(key, value)
                )
            return form_page(request, are_you_sure_form)

        # User has clicked submit with controlled good being yes or no
        validated_data, status_code = post_goods(request, data)

        if 'errors' in validated_data:
            if validated_data['errors']:
                return form_page(request, self.main_form, data=data, errors=validated_data.get('errors'))

        return redirect(reverse_lazy('goods:goods'))


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
        data = []

        files = request.FILES.getlist("file")
        if len(files) is not 1:
            return error_page(None, 'We had an issue uploading your files. Try again later.')
        file = files[0]
        data.append({
            'name': file.original_name,
            's3_key': file.name,
            'size': int(file.size / 1024) if file.size else 0,  # in kilobytes
            'description': request.POST['description'],
        })

        # Send LITE API the file information
        good_documents, status_code = post_good_documents(request, good_id, data)

        if 'errors' in good_documents:
            return error_page(None, 'We had an issue uploading your files. Try again later.')

        return redirect(reverse('goods:good', kwargs={'pk': good_id}))


class Document(TemplateView):
    def get(self, request, **kwargs):
        good_id = str(kwargs['pk'])
        file_pk = str(kwargs['file_pk'])

        get_good(request, good_id)
        document, status_code = get_good_document(request, good_id, file_pk)
        original_file_name = document['document']['name']

        # Stream file
        def generate_file(result):
            for chunk in iter(lambda: result['Body'].read(settings.STREAMING_CHUNK_SIZE), b''):
                yield chunk

        s3 = s3_client()
        s3_response = s3.get_object(Bucket=AWS_STORAGE_BUCKET_NAME, Key=document['document']['s3_key'])
        _kwargs = {}
        if s3_response.get('ContentType'):
            _kwargs['content_type'] = s3_response['ContentType']
        response = StreamingHttpResponse(generate_file(s3_response), **_kwargs)
        response['Content-Disposition'] = f'attachment; filename="{original_file_name}"'
        return response


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
