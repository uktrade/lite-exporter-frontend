from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from applications.forms import respond_to_query_form
from applications.services import get_applications, get_application, get_application_case_notes, \
    get_application_ecju_queries, get_application_ecju_query, put_application_ecju_query, post_application_case_notes
from core.services import get_notifications
from libraries.forms.generators import form_page, error_page


class ApplicationsList(TemplateView):
    def get(self, request, **kwargs):
        data, status_code = get_applications(request)
        notifications, _ = get_notifications(request, unviewed=True)
        notifications_ids_list = [x['application'] for x in notifications['results']]

        context = {
            'data': data,
            'title': 'Applications',
            'notifications': notifications_ids_list,
        }
        return render(request, 'applications/index.html', context)


class ApplicationDetailEmpty(TemplateView):
    def get(self, request, **kwargs):
        application_id = str(kwargs['pk'])
        return redirect(reverse_lazy('applications:application-detail', kwargs={'pk': application_id,
                                                                                'type': 'case-notes'}))


class ApplicationDetail(TemplateView):

    application_id = None
    application = None
    case_id = None
    view_type = None

    def dispatch(self, request, *args, **kwargs):
        self.application_id = str(kwargs['pk'])
        application, status_code = get_application(request, self.application_id)
        self.application = application['application']
        self.case_id = self.application['case']
        self.view_type = kwargs['type']

        if self.view_type != 'case-notes' and self.view_type != 'ecju-queries':
            return Http404

        return super(ApplicationDetail, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        open_queries, closed_queries = get_application_ecju_queries(request, self.case_id)
        data, status_code = get_application(request, pk=self.application_id)
        # add application number to next query
        notifications, _ = get_notifications(request, unviewed=True)
        notifications = len([x for x in notifications['results'] if x['application'] == self.case_id])

        context = {
            'application': self.application,
            'title': self.application['name'],
            'type': self.view_type,
            'open_queries': open_queries,
        }

        if notifications > 0:
            context['notifications'] = notifications

        if self.view_type == 'case-notes':
            context['notes'] = get_application_case_notes(request, self.case_id)['case_notes']

        if self.view_type == 'ecju-queries':
            context['closed_queries'] = closed_queries

        return render(request, 'applications/application.html', context)

    def post(self, request, **kwargs):
        if self.view_type != 'case-notes':
            return Http404

        response, status_code = post_application_case_notes(request, self.case_id, request.POST)

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

        return redirect(reverse_lazy('applications:application', kwargs={'pk': self.application_id}))


class RespondToQuery(TemplateView):
    def get(self, request, **kwargs):
        application_id = str(kwargs['pk'])
        ecju_query = get_application_ecju_query(request, str(kwargs['pk']), str(kwargs['query_pk']))

        if ecju_query['response']:
            raise Http404

        return form_page(request, respond_to_query_form(application_id, ecju_query))

    def post(self, request, **kwargs):
        application_id = str(kwargs['pk'])
        ecju_query_id = str(kwargs['query_pk'])
        ecju_query = get_application_ecju_query(request, application_id, ecju_query_id)

        data, status_code = put_application_ecju_query(request, str(kwargs['pk']), str(kwargs['query_pk']),
                                                       request.POST)

        if 'errors' in data:
            return form_page(request, respond_to_query_form(application_id, ecju_query), data=request.POST,
                             errors=data['errors'])

        return redirect(reverse_lazy('applications:application-detail', kwargs={'pk': application_id,
                                                                                'type': 'ecju-queries'}))
