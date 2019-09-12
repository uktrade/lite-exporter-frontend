import logging

from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from lite_forms.generators import form_page, error_page
from s3chunkuploader.file_handler import S3FileUploadHandler

from apply_for_a_licence.forms.end_user import attach_document_form, delete_document_confirmation_form
from apply_for_a_licence.services import add_document_data, download_document_from_s3
from conf.constants import STANDARD_LICENCE
from core.builtins.custom_tags import get_string
from drafts.services import get_draft, post_ultimate_end_user_document, post_end_user_document, \
    get_ultimate_end_user_document, get_end_user_document, delete_ultimate_end_user_document, delete_end_user_document


@method_decorator(csrf_exempt, 'dispatch')
class AttachDocuments(TemplateView):
    def get(self, request, **kwargs):
        draft_id = str(kwargs['pk'])
        draft, status_code = get_draft(request, draft_id)
        if status_code == 200:
            if draft.get('draft').get('licence_type').get('key') == STANDARD_LICENCE:
                if 'ultimate-end-user' in request.path:
                    back_text = get_string('ultimate_end_user.documents.attach_documents.back_to_application_overview')
                    draft_url = reverse('apply_for_a_licence:ultimate_end_users', kwargs={'pk': draft_id})
                    title = get_string('ultimate_end_user.documents.attach_documents.title')
                    return_later_text = get_string('ultimate_end_user.documents.save_end_user')
                else:
                    back_text = get_string('end_user.documents.attach_documents.back_to_application_overview')
                    draft_url = reverse('apply_for_a_licence:overview', kwargs={'pk': draft_id})
                    title = get_string('end_user.documents.attach_documents.title')
                    return_later_text = get_string('end_user.documents.save_end_user')

                form = attach_document_form(draft_url=draft_url, title=title,
                                            back_text=back_text, return_later_text=return_later_text)
                return form_page(request, form, extra_data={'draft_id': draft_id})
            else:
                return redirect(reverse_lazy('apply_for_a_licence:overview', kwargs={'pk': draft_id}))
        else:
            return error_page(None, 'Cannot find draft')

    @csrf_exempt
    def post(self, request, **kwargs):
        self.request.upload_handlers.insert(0, S3FileUploadHandler(request))
        logging.info(self.request)
        draft_id = str(kwargs['pk'])
        data, error = add_document_data(request)

        if error:
            return error_page(None, get_string('end_user.documents.attach_documents.upload_error'))

        # Send LITE API the file information
        if 'ultimate-end-user' in request.path:
            end_user_document, status_code = post_ultimate_end_user_document(request, draft_id,
                                                                             str(kwargs['ueu_pk']), data)
            next_page = 'apply_for_a_licence:ultimate_end_users'
        else:
            end_user_document, status_code = post_end_user_document(request, draft_id, data)
            next_page = 'apply_for_a_licence:overview'

        if status_code != 201:
            return error_page(None, get_string('end_user.documents.attach_documents.upload_error'))
        return redirect(reverse(next_page, kwargs={'pk': draft_id}))


class DownloadDocument(TemplateView):
    def get(self, request, **kwargs):
        draft_id = str(kwargs['pk'])

        if 'ultimate-end-user' in request.path:
            document, status_code = get_ultimate_end_user_document(request, draft_id, str(kwargs['ueu_pk']))
        else:
            document, status_code = get_end_user_document(request, draft_id)

        document = document['document']

        if document['safe']:
            return download_document_from_s3(document['s3_key'], document['name'])
        else:
            return error_page(None, get_string('end_user.documents.attach_documents.download_error'))


class DeleteDocument(TemplateView):
    def get(self, request, **kwargs):
        if 'ultimate-end-user' in request.path:
            back_address = 'apply_for_a_licence:ultimate_end_users'
            back_link_text = get_string('ultimate_end_user.documents.attach_documents.back_to_application_overview')
        else:
            back_address = 'apply_for_a_licence:overview'
            back_link_text = get_string('end_user.documents.attach_documents.back_to_application_overview')
        form = delete_document_confirmation_form(
            overview_url=reverse(back_address, kwargs={'pk': str(kwargs['pk'])}),
            back_link_text=back_link_text
        )

        return form_page(request, form)

    def post(self, request, **kwargs):
        draft_id = str(kwargs['pk'])
        option = request.POST.get('delete_document_confirmation')
        if option is None:
            return redirect(request.path_info, kwargs={'pk': draft_id})
        elif option == 'yes':
            if 'ultimate-end-user' in request.path:
                status_code = delete_ultimate_end_user_document(request, draft_id, str(kwargs['ueu_pk']))
            else:
                status_code = delete_end_user_document(request, draft_id)
            if status_code is not 204:
                return error_page(None, get_string('end_user.documents.attach_documents.delete_error'))

        if 'ultimate-end-user' in request.path:
            return redirect(reverse('apply_for_a_licence:ultimate_end_users', kwargs={'pk': str(kwargs['pk'])}))
        else:
            return redirect(reverse('apply_for_a_licence:overview', kwargs={'pk': draft_id}))