from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from lite_forms.components import HiddenField
from lite_forms.generators import form_page, error_page
from lite_forms.submitters import submit_paged_form

from applications.services import get_case_notes, get_application_ecju_queries, post_application_case_notes
from core.services import get_notifications
from end_users.forms import apply_for_an_end_user_advisory_form, copy_end_user_advisory_form, \
    end_user_advisory_success_page
from end_users.services import get_end_user_advisories, post_end_user_advisories, get_end_user_advisory


class EndUsersList(TemplateView):
    def get(self, request, **kwargs):
        end_users = get_end_user_advisories(request)

        context = {
            'title': 'End User Advisories',
            'end_users': end_users,
        }
        return render(request, 'end_users/end_users.html', context)


class CopyAdvisory(TemplateView):

    forms = None
    data = None

    def dispatch(self, request, *args, **kwargs):
        self.forms = copy_end_user_advisory_form()
        query, _ = get_end_user_advisory(request, str(kwargs['pk']))

        # Add the existing end user type as a hidden field to preserve its data
        self.forms.forms[0].questions.append(HiddenField('end_user.sub_type', query['end_user']['sub_type']['key']))

        self.data = {
            'end_user.name': query['end_user']['name'],
            'end_user.website': query['end_user']['website'],
            'end_user.address': query['end_user']['address'],
            'end_user.country': query['end_user']['country']['id'],
            'reasoning': query.get('reasoning', ''),
            'note': query.get('note', ''),
            'copy_of': query['id'],
        }

        return super(CopyAdvisory, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        return form_page(request, self.forms.forms[0], data=self.data)

    def post(self, request, **kwargs):
        response, data = submit_paged_form(request, self.forms, post_end_user_advisories, inject_data=self.data)

        if response:
            return response

        return end_user_advisory_success_page(request, str(data['end_user_advisory']['id']))


class ApplyForAnAdvisory(TemplateView):

    forms = None

    def dispatch(self, request, *args, **kwargs):
        self.forms = apply_for_an_end_user_advisory_form()

        return super(ApplyForAnAdvisory, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        return form_page(request, self.forms.forms[0])

    def post(self, request, **kwargs):
        response, data = submit_paged_form(request, self.forms, post_end_user_advisories)

        if response:
            return response

        return end_user_advisory_success_page(request, str(data['end_user_advisory']['id']))

class EndUserDetailEmpty(TemplateView):
    def get(self, request, **kwargs):
        return redirect(reverse_lazy('end_users:end_user_detail', kwargs={'pk': kwargs['pk'],
                                                                  'type': 'case-notes'}))


class EndUserDetail(TemplateView):
    end_user_advisory_id = None
    end_user_advisory = None
    view_type = None
    case_id = None

    def dispatch(self, request, *args, **kwargs):
        self.end_user_advisory_id = str(kwargs['pk'])
        self.end_user_advisory, self.case_id = get_end_user_advisory(request, self.end_user_advisory_id)
        self.view_type = kwargs['type']

        if self.view_type != 'case-notes' and self.view_type != 'ecju-queries':
            return Http404

        return super(EndUserDetail, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        notifications = get_notifications(request, unviewed=True)
        case_note_notifications = len([x for x in notifications if x['parent'] == self.end_user_advisory_id
                                       and x['object'] == 'case_note'])
        ecju_query_notifications = len([x for x in notifications if x['parent'] == self.end_user_advisory_id
                                        and x['object_type'] == 'ecju_query'])

        context = {
            'title': 'Good',
            'case_id': self.case_id,
            'end_user_advisory': self.end_user_advisory,
            'case_note_notifications': case_note_notifications,
            'ecju_query_notifications': ecju_query_notifications,
            'type': self.view_type
        }

        if self.view_type == 'case-notes':
            case_notes = get_case_notes(request, self.case_id)['case_notes']
            context['notes'] = filter(lambda note: note['is_visible_to_exporter'], case_notes)

        if self.view_type == 'ecju-queries':
            context['open_queries'], context['closed_queries'] = get_application_ecju_queries(request,
                                                                                              self.case_id)

        return render(request, 'end_users/end_user.html', context)

    def post(self, request, **kwargs):
        if self.view_type != 'case-notes':
            return Http404

        good_id = kwargs['pk']

        response, _ = post_application_case_notes(request, self.case_id, request.POST)

        if 'errors' in response:
            errors = response.get('errors')
            if errors.get('text'):
                error = errors.get('text')[0]
                error = error.replace('This field', 'Case note')
                error = error.replace('this field', 'the case note')  # TODO: Move to API

            else:
                error_list = []
                for key in errors:
                    error_list.append("{field}: {error}".format(field=key, error=errors[key][0]))
                error = "\n".join(error_list)
            return error_page(request, error)

        return redirect(reverse_lazy('end_users:end_user_detail', kwargs={'pk': self.end_user_advisory_id,
                                                                  'type': 'case-notes'}))