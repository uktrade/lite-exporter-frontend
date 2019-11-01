from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from lite_forms.components import HiddenField, Button
from lite_forms.generators import error_page
from s3chunkuploader.file_handler import S3FileUploadHandler
from django.utils.decorators import method_decorator

from applications.forms.goods import good_on_application_form, add_new_good_forms
from applications.services import get_application, get_application_goods, get_application_goods_types, \
    post_application_preexisting_goods, delete_application_preexisting_good, validate_application_good, \
    add_document_data
from core.services import get_units
from goods.services import get_goods, get_good, validate_good, post_good, post_good_documents


class DraftGoodsList(TemplateView):
    def get(self, request, **kwargs):
        """
        List all goods related to the draft
        """
        draft_id = str(kwargs['pk'])
        application = get_application(request, draft_id)
        goods = get_application_goods(request, draft_id)

        context = {
            'goods': goods,
            'application': application
        }
        return render(request, 'applications/goods/index.html', context)


class GoodsList(TemplateView):
    def get(self, request, **kwargs):
        """
        List of existing goods  (add-preexisting)
        """
        application_id = str(kwargs['pk'])
        application = get_application(request, application_id)
        description = request.GET.get('description', '').strip()
        part_number = request.GET.get('part_number', '').strip()
        control_rating = request.GET.get('control_rating', '').strip()
        goods_list, _ = get_goods(request, {'description': description,
                                            'part_number': part_number,
                                            'control_rating': control_rating})

        filtered_data = []
        for good in goods_list:
            if good['documents'] and not good['is_good_controlled'] == 'unsure':
                filtered_data.append(good)

        context = {
            'application': application,
            'data': filtered_data,
            'description': description,
            'part_number': part_number,
            'control_code': control_rating,
            'draft_id': application_id
        }
        return render(request, 'applications/goods/preexisting.html', context)


@method_decorator(csrf_exempt, 'dispatch')
class AddNewGood(TemplateView):
    form = None
    application_id = None
    context = None
    form_details = [
        {
            'name': 'good_details',
            'fields': ['description', 'control_code', 'part_number', 'is_good_controlled', 'is_good_end_product'],
            'validation_function': validate_good,
            'prefix': 'good_'  # Prefix needed to distinguish fields with same names on multiple forms
        },
        {
            'name': 'good_on_application_details',
            'fields': ['value', 'quantity', 'unit'],
            'validation_function': validate_application_good,
            'prefix': 'good_on_app_'
        },
        {
            'name': 'good_document',
            'fields': []
        }
    ]

    def dispatch(self, request, *args, **kwargs):

        self.context = {'title': 'Add Good'}

        return super(AddNewGood, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        self.application_id = str(kwargs['pk'])
        self.generate_form(request, 0, -1)
        self.context['page'] = self.form
        return render(request, 'form.html', self.context)

    @csrf_exempt
    def post(self, request, **kwargs):
        # This has to be run at the top of the method before POST is accessed.
        self.request.upload_handlers.insert(0, S3FileUploadHandler(request))

        self.application_id = str(kwargs['pk'])
        form_names = list(map(lambda f: f['name'], self.form_details))
        form_num = form_names.index(request.POST.get('form_name'))

        if request.POST.get('actions', None) == 'back':
            self.generate_form(request, form_num-1, form_num)

        elif form_num == 0:
            self.handle_post_for_form(request, form_num)

        elif form_num == 1:
            self.handle_post_for_form(request, form_num, pk=self.application_id)

        elif form_num == 2:
            if request.FILES:
                # post good
                post_data = self.extract_data_from_hidden_fields(request.POST, 0)

                validated_data, status_code = post_good(request, post_data)

                if status_code != 201:
                    raise Http404

                # attach document
                good_id = validated_data['good']['id']
                data, error = add_document_data(request)

                if error:
                    return error_page(None, error)

                # Send LITE API the file information
                good_documents, _ = post_good_documents(request, good_id, [data])

                # Attach good to application
                post_data = self.extract_data_from_hidden_fields(request.POST, 1)
                post_data['good_id'] = good_id

                _, _ = post_application_preexisting_goods(request, self.application_id, post_data)

                return redirect('applications:goods', self.application_id)
            else:
                self.generate_form(request, form_num, form_num)
                self.context['errors'] = {'': ['A document is required.']}

        self.context['page'] = self.form

        return render(request, 'form.html', self.context)

    def handle_post_for_form(self, request, form_num, pk=None):
        post = {}

        # Set the fields for the POST request relating to validation
        for field in self.form_details[form_num]['fields']:
            post[field] = request.POST.get(field, None)

        # Call the relevant validation function for the form that posted.
        if pk:
            data = self.form_details[form_num]['validation_function'](request, pk, json=post)
        else:
            data = self.form_details[form_num]['validation_function'](request, json=post)

        if data.status_code != 200:
            self.generate_form(request, form_num, form_num)
            self.context['errors'] = data.json()['errors']
            self.context['data'] = post
        else:
            self.generate_form(request, (form_num + 1), form_num)

    def generate_form(self, request, destination_form, originating_form):
        self.form = add_new_good_forms(request, self.application_id)[destination_form]
        self.form.questions.append(HiddenField('form_name', value=self.form_details[destination_form]['name']))
        if destination_form != len(self.form_details) - 1:  # Final form should use the default save button
            self.form.buttons = [Button('Continue', 'continue')]

        if originating_form != -1:  # If this isn't the first form we've visited
            # Use request.POST as the source for hidden fields so that all data from all forms to date is added
            self.add_hidden_fields(request.POST, originating_form)
            self.context['data'] = self.extract_data_from_hidden_fields(request.POST, destination_form)

    def add_hidden_fields(self, post, originating_form):
        self.add_hidden_details_fields(post, 0, originating_form)
        self.add_hidden_details_fields(post, 1, originating_form)

    def add_hidden_details_fields(self, post, form_to_process_num, originating_form):
        fields = self.form_details[form_to_process_num]['fields']
        prefix = self.form_details[form_to_process_num]['prefix']

        for field in fields:
            field_value_from_posted_form = post.get(field, '')

            if form_to_process_num == originating_form:
                self.form.questions.append(HiddenField(prefix + field, value=field_value_from_posted_form))
            else:
                field_value_from_hidden_field = post.get(prefix + field, None)

                if field_value_from_hidden_field or field_value_from_hidden_field == '':
                    self.form.questions.append(HiddenField((prefix + field), value=field_value_from_hidden_field))

    def extract_data_from_hidden_fields(self, post, destination_form_num):
        data = {}

        for field in self.form_details[destination_form_num]['fields']:
            data[field] = post.get((self.form_details[destination_form_num]['prefix'] + field), None)

        return data


class DraftOpenGoodsTypeList(TemplateView):
    def get(self, request, **kwargs):
        application_id = str(kwargs['pk'])
        application = get_application(request, application_id)
        goods = get_application_goods_types(request, application_id)

        context = {
            'goods': goods,
            'application': application,
        }
        return render(request, 'applications/goodstype/index.html', context)


class AddPreexistingGood(TemplateView):
    def get(self, request, **kwargs):
        good, _ = get_good(request, str(kwargs['good_pk']))

        context = {
            'title': 'Add a pre-existing good to your application',
            'page': good_on_application_form(good, get_units(request))
        }
        return render(request, 'form.html', context)

    def post(self, request, **kwargs):
        draft_id = str(kwargs['pk'])
        data, status_code = post_application_preexisting_goods(request, draft_id, request.POST)

        if status_code != 201:
            good, status_code = get_good(request, str(kwargs['good_pk']))

            context = {
                'title': 'Add a pre-existing good to your application',
                'page': good_on_application_form(good, get_units(request)),
                'data': request.POST,
                'errors': data.get('errors'),
            }
            return render(request, 'form.html', context)

        return redirect(reverse_lazy('applications:goods', kwargs={'pk': draft_id}))


class RemovePreexistingGood(TemplateView):
    def get(self, request, **kwargs):
        application_id = str(kwargs['pk'])
        good_on_application_id = str(kwargs['good_on_application_pk'])

        status_code = delete_application_preexisting_good(request, good_on_application_id)

        if status_code != 200:
            return error_page(request, 'Unexpected error removing good')

        return redirect(reverse_lazy('applications:goods', kwargs={'pk': application_id}))
