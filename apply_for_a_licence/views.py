from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from apply_for_a_licence import forms
from core.builtins.custom_tags import get_string
from drafts.services import post_drafts, get_draft
from libraries.forms.components import HiddenField
from libraries.forms.helpers import get_form_by_pk, get_next_form_after_pk, nest_data, remove_unused_errors


class StartApplication(TemplateView):
    def get(self, request, **kwargs):
        context = {
            'title': get_string('licences.apply_for_a_licence'),
            'service_uses': get_string('licences.use_this_service_to'),
        }
        return render(request, 'apply_for_a_licence/index.html', context)


class InitialQuestions(TemplateView):
    def get(self, request, **kwargs):
        context = {
            'page': forms.initial_questions.forms[0],
            'title': forms.initial_questions.forms[0].title,
        }
        return render(request, 'form.html', context)

    def post(self, request, **kwargs):
        data = request.POST.copy()

        # Get the next form based off form_pk
        current_form = get_form_by_pk(data.get('form_pk'), forms.initial_questions)
        next_form = get_next_form_after_pk(data.get('form_pk'), forms.initial_questions)

        # Remove form_pk and CSRF from POST data as the new form will replace them
        del data['form_pk']
        del data['csrfmiddlewaretoken']

        # Post the data to the validator and check for errors
        nested_data = nest_data(data)
        validated_data, status_code = post_drafts(request, nested_data)

        if 'errors' in validated_data:
            validated_data['errors'] = remove_unused_errors(validated_data['errors'], current_form)

            # If there are errors in the validated data, take the user back
            if len(validated_data['errors']) is not 0:
                context = {
                    'page': current_form,
                    'title': current_form.title,
                    'errors': validated_data['errors'],
                    'data': data,
                }
                return render(request, 'form.html', context)

        # If there aren't any forms left to go through, submit all the data and go to the overview page
        if next_form is None:
            draft_pk = validated_data['draft']['id']
            return redirect(reverse_lazy('apply_for_a_licence:overview', kwargs={'pk': draft_pk}))

        # Add existing post data to new form as hidden fields
        for key, value in data.items():
            next_form.questions.append(
                HiddenField(key, value)
            )

        # Go to the next page
        context = {
            'page': next_form,
            'title': next_form.title,
        }
        return render(request, 'form.html', context)


class Overview(TemplateView):
    def get(self, request, **kwargs):
        data, status_code = get_draft(request, str(kwargs['pk']))

        context = {
            'title': 'Draft Overview',
            'data': data,
        }
        return render(request, 'apply_for_a_licence/overview.html', context)
