from django.urls import reverse

from core.services import get_countries
from libraries.forms.components import Form, Checkboxes, Filter, BackLink


def countries_form(draft_id):
    return Form(title='Where are your goods going?',
                description='Select all countries that apply.',
                questions=[
                    Filter(),
                    Checkboxes('countries', get_countries(None, True), classes=['govuk-checkboxes--small']),
                ],
                javascript_imports=['/assets/javascripts/filter-checkbox-list.js'],
                back_link=BackLink('Back to Overview', reverse('apply_for_a_licence:overview',
                                                               kwargs={'pk': draft_id})))
