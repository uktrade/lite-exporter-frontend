from django.shortcuts import render
from django.views.generic import TemplateView

from applications.services import get_additional_documents


class AdditionalDocuments(TemplateView):
    def get(self, request, **kwargs):
        draft_id = str(kwargs['pk'])
        data, _ = get_additional_documents(request, draft_id)

        context = {
            'additional_documents': data['documents'],
            'draft_id': draft_id,
            'download_document_link': 'applications:download_additional_document',
            'delete_document_link': 'applications:delete_additional_document',
            'attach_document_link': 'applications:attach_additional_document',
            'title': 'Additional Documents'
        }

        return render(request, 'apply_for_a_licence/additional_documents/additional_documents.html', context)
