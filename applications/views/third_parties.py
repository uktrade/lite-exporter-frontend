from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from applications.libraries.check_your_answers_helpers import _convert_consignee
from lite_forms.generators import form_page, error_page
from lite_forms.submitters import submit_paged_form

from applications.forms.end_user import new_consignee_forms
from applications.forms.third_party import third_party_forms
from applications.services import post_third_party, get_third_parties, delete_third_party, post_consignee, \
    get_application, delete_consignee
from lite_forms.views import MultiFormView


class AddThirdParty(TemplateView):
    draft_id = None
    form = None

    def dispatch(self, request, *args, **kwargs):
        self.draft_id = str(kwargs['pk'])
        draft = get_application(request, self.draft_id)
        self.form = third_party_forms(draft.get('export_type'))

        return super(AddThirdParty, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        return form_page(request, self.form.forms[0])

    def post(self, request, **kwargs):
        response, data = submit_paged_form(request, self.form, post_third_party, object_pk=self.draft_id)

        if response:
            return response

        return redirect(reverse_lazy('applications:third_party_attach_document',
                                     kwargs={'pk': self.draft_id, 'tp_pk': data['third_party']['id']}))


class ThirdParties(TemplateView):
    def get(self, request, **kwargs):
        application_id = str(kwargs['pk'])
        application = get_application(request, application_id)

        if not application['third_parties']:
            return redirect(reverse_lazy('applications:add_third_party', kwargs={'pk': application_id}))

        context = {
            'application': application,
            'third_parties': application['third_parties'],
        }
        return render(request, 'applications/parties/third_parties.html', context)


class RemoveThirdParty(TemplateView):
    def get(self, request, **kwargs):
        draft_id = str(kwargs['pk'])
        ueu_pk = str(kwargs['ueu_pk'])
        delete_third_party(request, draft_id, ueu_pk)
        return redirect(reverse_lazy('applications:third_parties', kwargs={'pk': draft_id}))


class Consignee(TemplateView):
    def get(self, request, **kwargs):
        application_id = str(kwargs['pk'])
        application = get_application(request, application_id)

        if application['consignee']:
            context = {
                'application': application,
                'title': 'Consignee',
                'edit_url': reverse_lazy('applications:set_consignee', kwargs={'pk': application_id}),
                'remove_url': reverse_lazy('applications:remove_consignee', kwargs={'pk': application_id}),
                'answers': _convert_consignee(application['consignee']),
            }
            return render(request, 'applications/check-your-answer.html', context)
        else:
            return redirect(reverse_lazy('applications:set_consignee', kwargs={'pk': application_id}))


class SetConsignee(MultiFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs['pk']
        self.data = get_application(request, self.object_pk)['end_user']
        self.forms = new_consignee_forms()
        self.action = post_consignee
        self.success_url = reverse_lazy('applications:consignee_attach_document', kwargs={'pk': self.object_pk})


class RemoveConsignee(TemplateView):
    def get(self, request, **kwargs):
        application_id = str(kwargs['pk'])
        status_code = delete_consignee(request, application_id)

        if status_code != 204:
            return error_page(request, 'Unexpected error removing consignee')

        return redirect(reverse_lazy('applications:task_list', kwargs={'pk': application_id}))
