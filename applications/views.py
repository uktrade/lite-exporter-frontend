from http import HTTPStatus

from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView
from lite_forms.components import HiddenField
from lite_forms.generators import error_page, form_page

from applications.forms import respond_to_query_form, ecju_query_respond_confirmation_form, edit_type_form
from applications.services import get_applications, get_application, get_case_notes, \
    get_application_ecju_queries, get_ecju_query, put_ecju_query, post_application_case_notes, set_application_status
from apply_for_a_licence.views.common import get_licence_overview
from core.helpers import group_notifications
from core.services import get_notifications


class ApplicationsList(TemplateView):
    def get(self, request, **kwargs):
        applications = get_applications(request)
        notifications = get_notifications(request, unviewed=True)

        context = {
            'title': 'Applications',
            'applications': applications,
            'notifications': group_notifications(notifications),
        }
        return render(request, 'applications/index.html', context)


class ApplicationDetailEmpty(TemplateView):
    def get(self, request, **kwargs):
        application_id = str(kwargs['pk'])
        data, _ = get_application(request, application_id)

        if data.get('application').get('status') == 'applicant_editing':
            return redirect(reverse_lazy('applications:application-edit-overview', kwargs={'pk': application_id}))

        return redirect(reverse_lazy('applications:application-detail', kwargs={'pk': application_id,
                                                                                'type': 'case-notes'}))


class ApplicationEditType(TemplateView):

    def get(self, request, **kwargs):
        application_id = str(kwargs['pk'])
        data, _ = get_application(request, application_id)

        if data.get('application').get('status') == 'applicant_editing':
            return redirect(reverse_lazy('applications:application-edit-overview', kwargs={'pk': application_id}))

        return form_page(request, edit_type_form(application_id))

    def post(self, request, **kwargs):
        if request.POST.get('edit-type') == 'major':
            data, status_code = set_application_status(request, str(kwargs['pk']), 'applicant_editing')

            if status_code != HTTPStatus.OK:
                return form_page(request, edit_type_form(str(kwargs['pk'])), errors=data)

        return redirect(reverse_lazy('applications:application-edit-overview', kwargs={'pk': str(kwargs['pk'])}))


class ApplicationEditOverview(TemplateView):
    def get(self, request, **kwargs):
        application_data, status_code = get_application(request, str(kwargs['pk']))

        if status_code != HTTPStatus.OK:
            # Wasn't able to get application so redirecting to exporter hub
            return redirect(reverse('core:hub'))

        return get_licence_overview(request, application=application_data.get('application'))

    # def post(self, request, **kwargs):
    #
    #     if post to api is successful:
    #         return 'application-edit-overview'
    #     else:
    #         return 'some-template.html'


class ApplicationDetail(TemplateView):
    application_id = None
    application = None
    case_id = None
    view_type = None

    def dispatch(self, request, *args, **kwargs):
        self.application_id = str(kwargs['pk'])
        application, _ = get_application(request, self.application_id)
        self.application = application['application']
        self.case_id = self.application['case']
        self.view_type = kwargs['type']

        if self.view_type != 'case-notes' and self.view_type != 'ecju-queries':
            return Http404

        return super(ApplicationDetail, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        # add application number to next query
        notifications = get_notifications(request, unviewed=True)
        case_note_notifications = len([x for x in notifications if x['parent'] == self.application_id
                                       and x['object_type'] == 'case_note'])
        ecju_query_notifications = len([x for x in notifications if x['parent'] == self.application_id
                                        and x['object_type'] == 'ecju_query'])

        context = {
            'application': self.application,
            'title': self.application['name'],
            'type': self.view_type,
            'case_note_notifications': case_note_notifications,
            'ecju_query_notifications': ecju_query_notifications,
        }

        if self.view_type == 'case-notes':
            context['notes'] = get_case_notes(request, self.case_id)['case_notes']

        if self.view_type == 'ecju-queries':
            context['open_queries'], context['closed_queries'] = get_application_ecju_queries(request, self.case_id)

        return render(request, 'applications/application.html', context)

    def post(self, request, **kwargs):
        if self.view_type != 'case-notes':
            return Http404

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
                    error_list.append('{field}: {error}'.format(field=key, error=errors[key][0]))
                error = '\n'.join(error_list)
            return error_page(request, error)

        return redirect(reverse_lazy('applications:application', kwargs={'pk': self.application_id}))


class RespondToQuery(TemplateView):
    application_id = None
    ecju_query_id = None
    ecju_query = None

    def dispatch(self, request, *args, **kwargs):
        self.application_id = str(kwargs['pk'])
        self.ecju_query_id = str(kwargs['query_pk'])
        self.ecju_query = get_ecju_query(request, str(kwargs['pk']), str(kwargs['query_pk']))

        if self.ecju_query['response']:
            return redirect(reverse_lazy('applications:application-detail', kwargs={'pk': self.application_id,
                                                                                    'type': 'ecju-queries'}))

        return super(RespondToQuery, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        """
        Will get a text area form for the user to respond to the ecju_query
        """
        return form_page(request, respond_to_query_form(self.application_id, self.ecju_query))

    def post(self, request, **kwargs):
        """
        will determine what form the user is on:
        if the user is on the input form will then will determine if data is valid, and move user to confirmation form
        else will allow the user to confirm they wish to respond and post data if accepted.
        """
        form_name = request.POST.get('form_name')

        if form_name == 'respond_to_query':
            # Post the form data to API for validation only
            data = {'response': request.POST.get('response'), 'validate_only': True}
            response, status_code = put_ecju_query(request, self.application_id, self.ecju_query_id, data)

            if status_code != HTTPStatus.OK:
                errors = response.get('errors')
                errors = {error: message for error, message in errors.items()}
                form = respond_to_query_form(self.application_id, self.ecju_query)
                data = {'response': request.POST.get('response')}
                return form_page(request, form, data=data, errors=errors)
            else:
                form = ecju_query_respond_confirmation_form(reverse_lazy('applications:respond_to_query',
                                                                         kwargs={'pk': self.application_id,
                                                                                 'query_pk': self.ecju_query_id}))
                form.questions.append(HiddenField('response', request.POST.get('response')))
                return form_page(request, form)
        elif form_name == 'ecju_query_response_confirmation':
            if request.POST.get('confirm_response') == 'yes':
                data, status_code = put_ecju_query(request, self.application_id, self.ecju_query_id,
                                                   request.POST)

                if 'errors' in data:
                    return form_page(request, respond_to_query_form(self.application_id, self.ecju_query),
                                     data=request.POST,
                                     errors=data['errors'])

                return redirect(reverse_lazy('applications:application-detail', kwargs={'pk': self.application_id,
                                                                                        'type': 'ecju-queries'}))
            elif request.POST.get('confirm_response') == 'no':
                return form_page(request, respond_to_query_form(self.application_id, self.ecju_query),
                                 data=request.POST)
            else:
                error = {'required': ['This field is required']}
                form = ecju_query_respond_confirmation_form(reverse_lazy('applications:respond_to_query',
                                                                         kwargs={'pk': self.application_id,
                                                                                 'query_pk': self.ecju_query_id}))
                form.questions.append(HiddenField('response', request.POST.get('response')))
                return form_page(request, form, errors=error)
        else:
            # Submitted data does not contain an expected form field - return an error
            return error_page(None, 'We had an issue creating your response. Try again later.')
