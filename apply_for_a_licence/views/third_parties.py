from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from lite_forms.generators import form_page
from lite_forms.submitters import submit_paged_form

from apply_for_a_licence.forms.third_party import third_party_forms
from apply_for_a_licence.helpers import create_persistent_bar
from drafts.services import get_draft, get_ultimate_end_users, post_third_party


class AddThirdParty(TemplateView):
    draft_id = None
    form = None

    def dispatch(self, request, *args, **kwargs):
        self.draft_id = str(kwargs['pk'])
        self.form = third_party_forms()

        return super(AddThirdParty, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        draft, status_code = get_draft(request, self.draft_id)

        return form_page(request, self.form.forms[0], extra_data={
            'persistent_bar': create_persistent_bar(draft.get('draft'))
        })

    def post(self, request, **kwargs):
        response, data = submit_paged_form(request, self.form, post_third_party, pk=self.draft_id)

        if response:
            return response

        return redirect(reverse_lazy('apply_for_a_licence:ultimate_end_user_attach_document',
                                     kwargs={'pk': self.draft_id, 'ueu_pk': data['end_user']['id']}))


class ThirdParties(TemplateView):
    def get(self, request, **kwargs):
        draft_id = str(kwargs['pk'])
        data, status_code = get_ultimate_end_users(request, draft_id)

        context = {
            'third_parties': data['ultimate_end_users'],
            'draft_id': draft_id,
            'title': 'Third parties',
            'description': 'add third parties ... TODO',
            'entity_name': 'third party',
            'add_link': 'apply_for_a_licence:add_third_party',
            'download_document_link': 'apply_for_a_licence:ultimate_end_user_download_document',
            'delete_document_link': 'apply_for_a_licence:ultimate_end_user_delete_document',
            'attach_document_link': 'apply_for_a_licence:ultimate_end_user_attach_document',
            'delete_link': 'apply_for_a_licence:remove_ultimate_end_user'
        }

        return render(request, 'apply_for_a_licence/parties/index.html', context)
