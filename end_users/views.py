from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from lite_forms.generators import form_page
from lite_forms.submitters import submit_paged_form

from end_users.forms import apply_for_an_end_user_advisory_form
from end_users.services import get_end_user_advisories, post_end_user_advisories


class EndUsersList(TemplateView):
    def get(self, request, **kwargs):
        end_users = get_end_user_advisories(request)

        context = {
            'title': 'End Users',
            'end_users': end_users,
        }
        return render(request, 'end_users/index.html', context)


class ApplyForAnAdvisory(TemplateView):

    forms = None

    def dispatch(self, request, *args, **kwargs):
        self.forms = apply_for_an_end_user_advisory_form()

        return super(ApplyForAnAdvisory, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        return form_page(request, self.forms.forms[0])

    def post(self, request, **kwargs):
        response, data = submit_paged_form(request, self.forms, post_end_user_advisories)

        # If there are more forms to go through, continue
        if response:
            return response

        return redirect('end_users:end_users')
