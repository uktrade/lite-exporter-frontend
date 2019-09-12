from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from lite_forms.generators import form_page
from lite_forms.submitters import submit_paged_form

from apply_for_a_licence.forms.third_party import third_party_forms
from apply_for_a_licence.helpers import create_persistent_bar
from drafts.services import get_draft, post_third_party, get_third_parties, delete_third_party


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

        return redirect(reverse_lazy('apply_for_a_licence:third_parties',
                                     kwargs={'pk': self.draft_id}))


class ThirdParties(TemplateView):
    def get(self, request, **kwargs):
        draft_id = str(kwargs['pk'])
        data, status_code = get_third_parties(request, draft_id)

        context = {
            'third_parties': data['third_parties'],
            'draft_id': draft_id,
            'description': 'add third parties ... TODO',
            'add_link': 'apply_for_a_licence:add_third_party',
            'delete_link': 'apply_for_a_licence:remove_third_party'
        }

        return render(request, 'apply_for_a_licence/parties/third_parties.html', context)


class RemoveThirdParty(TemplateView):
    def get(self, request, **kwargs):
        draft_id = str(kwargs['pk'])
        ueu_pk = str(kwargs['ueu_pk'])
        delete_third_party(request, draft_id, ueu_pk)
        return redirect(reverse_lazy('apply_for_a_licence:third_parties', kwargs={'pk': draft_id}))
