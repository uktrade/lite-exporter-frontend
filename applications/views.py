from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from applications.forms import respond_to_query_form
from applications.services import get_applications, get_application, get_application_case_notes, \
    get_application_ecju_queries, get_application_ecju_query, put_application_ecju_query
from core.services import get_notifications
from libraries.forms.generators import form_page


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
    def get(self, request, **kwargs):
        application_id = str(kwargs['pk'])
        application, status_code = get_application(request, application_id)
        application = application['application']
        case_id = application['case']
        view_type = kwargs['type']

        context = {
            'application': application,
            'title': application['name'],
            'type': view_type,
        }

        if view_type == 'case-notes':
            context['notes'] = get_application_case_notes(request, case_id)['case_notes']

        if view_type == 'ecju-queries':
            open_queries, closed_queries = get_application_ecju_queries(request, case_id)
            context['open_queries'] = open_queries
            context['closed_queries'] = closed_queries

        return render(request, 'applications/application.html', context)


class RespondToQuery(TemplateView):
    def get(self, request, **kwargs):
        application_id = str(kwargs['pk'])
        ecju_query = get_application_ecju_query(request, str(kwargs['pk']), str(kwargs['query_pk']))

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
                                                                                'type': 'ecju-query'}))


class CaseNotes(TemplateView):
    def post(self, request, **kwargs):
        application_id = str(kwargs['pk'])
        data, status_code = get_application(request, application_id)
        case_id = data['application']['case']

        # response, status_code = post_application_notes(request, case_id, request.POST)

        # if status_code != 201:
        #     errors = response.get('errors')
        #     if errors.get('text'):
        #         error = errors.get('text')[0]
        #         error = error.replace('This field', 'Case note')
        #         error = error.replace('this field', 'the case note')  # TODO: Move to API
        #
        #     else:
        #         error_list = []
        #         for key in errors:
        #             error_list.append("{field}: {error}".format(field=key, error=errors[key][0]))
        #         error = "\n".join(error_list)
        #     return error_page(request, error)

        return redirect(reverse_lazy('applications:application', kwargs={'pk': application_id}))
