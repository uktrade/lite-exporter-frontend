from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from lite_forms.generators import form_page
from lite_forms.submitters import submit_single_form

from applications.forms.countries import countries_form
from applications.forms.location import which_location_form, new_location_form, external_locations_form
from applications.forms.sites import sites_form
from core.services import get_sites_on_draft, post_sites_on_draft, post_external_locations, \
    get_external_locations_on_draft, get_external_locations, post_external_locations_on_draft
from applications.services import get_application, get_application_countries, post_application_countries


class Location(TemplateView):
    def get(self, request, **kwargs):
        application_id = str(kwargs['pk'])
        application = get_application(request, application_id)
        external_locations, _ = get_external_locations_on_draft(request, application_id)

        print(application['status'])

        if external_locations['external_locations']:
            data = {'organisation_or_external': 'external'}

            if application['status'].get('key') == 'submitted':
                return redirect(reverse_lazy('applications:external_locations', kwargs={'pk': application_id}))
        else:
            data = {'organisation_or_external': 'organisation'}

            if application['status'].get('key') == 'submitted':
                return redirect(reverse_lazy('applications:existing_sites', kwargs={'pk': application_id}))

        return form_page(request, which_location_form(application_id), data=data)

    def post(self, request, **kwargs):
        draft_id = str(kwargs['pk'])

        data = request.POST.copy()

        if 'organisation_or_external' not in data:
            errors = {
                'organisation_or_external': ['Select which one you want']
            }

            return form_page(request, which_location_form(draft_id), errors=errors)

        if data['organisation_or_external'] == 'external':
            return redirect(reverse_lazy('applications:external_locations', kwargs={'pk': draft_id}))
        else:
            return redirect(reverse_lazy('applications:existing_sites', kwargs={'pk': draft_id}))


# Existing Sites


class ExistingSites(TemplateView):
    def get(self, request, **kwargs):
        application_id = str(kwargs['pk'])
        application = get_application(request, application_id)
        response, _ = get_sites_on_draft(request, application_id)

        if application['status'].get('key') == 'submitted' and not response['sites']:
            raise Http404

        return form_page(request, sites_form(request), data=response)

    def post(self, request, **kwargs):
        draft_id = str(kwargs['pk'])
        data = {
            'sites': request.POST.getlist('sites')
        }

        response, status_code = post_sites_on_draft(request, draft_id, data)

        if status_code != 201:
            return form_page(request, sites_form(request), errors=response.get('errors'), data=data)

        return redirect(reverse_lazy('applications:edit', kwargs={'pk': draft_id}))


# External Locations


class ExternalLocations(TemplateView):
    def get(self, request, **kwargs):
        application_id = str(kwargs['pk'])
        application = get_application(request, application_id)
        org_external_locations, _ = get_external_locations(request, request.user.organisation)
        data, _ = get_external_locations_on_draft(request, application_id)

        if application['status'].get('key') == 'submitted' and not data['external_locations']:
            raise Http404

        context = {
            'title': 'External Locations',
            'org_external_locations': org_external_locations,
            'draft_id': application_id,
            'data': data,
            'draft': application,
        }
        return render(request, 'applications/external_locations/index.html', context)


class AddExternalLocation(TemplateView):
    def get(self, request, **kwargs):
        draft_id = str(kwargs['pk'])
        response, _ = get_sites_on_draft(request, draft_id)

        return form_page(request, new_location_form(), data=response)

    def post(self, request, **kwargs):
        draft_id = str(kwargs['pk'])
        response, response_data = submit_single_form(request, new_location_form(), post_external_locations,
                                                     pk=str(request.user.organisation))

        # If there are more forms to go through, continue
        if response:
            return response
        id = response_data['external_location']['id']

        # Append the new external location to the list of external locations rather than clearing them
        data = {
            'external_locations': [id],
            'method': 'append_location'
        }
        post_external_locations_on_draft(request, draft_id, data)

        # If there is no response (no forms left to go through), go to the overview page
        return redirect(reverse_lazy('applications:external_locations', kwargs={'pk': draft_id}))


class AddExistingExternalLocation(TemplateView):
    def get(self, request, **kwargs):
        draft_id = str(kwargs['pk'])
        data, _ = get_external_locations_on_draft(request, draft_id)

        return form_page(request, external_locations_form(request), data=data)

    def post(self, request, **kwargs):
        draft_id = str(kwargs['pk'])

        data = {
            'external_locations': request.POST.getlist('external_locations')
        }

        response, status_code = post_external_locations_on_draft(request, draft_id, data)

        if status_code != 201:
            return form_page(request, external_locations_form(request), errors=response.get('errors'))

        return redirect(reverse_lazy('applications:external_locations', kwargs={'pk': draft_id}))


# Countries


class Countries(TemplateView):
    def get(self, request, **kwargs):
        draft_id = str(kwargs['pk'])
        countries = {'countries': get_application_countries(request, draft_id)}

        return form_page(request, countries_form(draft_id), data=countries)

    def post(self, request, **kwargs):
        draft_id = str(kwargs['pk'])

        data = {
            'countries': request.POST.getlist('countries')
        }

        response, _ = submit_single_form(request, countries_form(draft_id), post_application_countries,
                                         pk=draft_id, override_data=data)

        if response:
            return response

        return redirect(reverse_lazy('applications:edit', kwargs={'pk': draft_id}))
