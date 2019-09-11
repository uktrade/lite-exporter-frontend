import logging

from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from s3chunkuploader.file_handler import S3FileUploadHandler

from apply_for_a_licence.forms.end_user import attach_document_form, delete_document_confirmation_form
from lite_forms.generators import form_page, success_page, error_page
from lite_forms.submitters import submit_paged_form

from apply_for_a_licence.forms import initial, goods
from apply_for_a_licence.forms.end_user import new_end_user_forms
from apply_for_a_licence.forms.ultimate_end_user import new_ultimate_end_user_form
from apply_for_a_licence.helpers import create_persistent_bar
from core.builtins.custom_tags import get_string
from core.services import get_units, get_sites_on_draft, get_external_locations_on_draft
from drafts.services import post_drafts, get_draft, get_draft_goods, post_draft_preexisting_goods, submit_draft, \
    delete_draft, post_end_user, get_draft_countries, get_draft_goods_type, get_ultimate_end_users, \
    post_ultimate_end_user, delete_ultimate_end_user, get_end_user_document, \
    delete_end_user_document, post_ultimate_end_user_document, post_end_user_document, get_ultimate_end_user_document, \
    delete_ultimate_end_user_document
from goods.services import get_goods, get_good
from apply_for_a_licence.services import add_document_data
from conf.constants import STANDARD_LICENCE
from apply_for_a_licence.services import download_document_from_s3


class StartApplication(TemplateView):
    def get(self, request, **kwargs):
        context = {
            'title': get_string('licences.apply_for_a_licence'),
            'service_uses': get_string('licences.use_this_service_to'),
        }
        return render(request, 'apply_for_a_licence/index.html', context)


class InitialQuestions(TemplateView):
    def get(self, request, **kwargs):
        return form_page(request, initial.initial_questions.forms[0])

    def post(self, request, **kwargs):
        response, data = submit_paged_form(request, initial.initial_questions, post_drafts)

        # If there are more forms to go through, continue
        if response:
            return response

        # If there is no response (no forms left to go through), go to the overview page
        return redirect(reverse_lazy('apply_for_a_licence:overview', kwargs={'pk': data['draft']['id']}))


class Overview(TemplateView):
    def get(self, request, **kwargs):
        draft_id = str(kwargs['pk'])
        data, status_code = get_draft(request, draft_id)
        sites, status_code = get_sites_on_draft(request, draft_id)
        goods, status_code = get_draft_goods(request, draft_id)
        ultimate_end_users_required = False
        countries, status_code = get_draft_countries(request, draft_id)
        goodstypes, status_code = get_draft_goods_type(request, draft_id)
        external_locations, status_code = get_external_locations_on_draft(request, draft_id)
        ultimate_end_users, status_code = get_ultimate_end_users(request, draft_id)
        end_user = data.get('draft').get('end_user')
        if end_user:
            end_user_document, status_code = get_end_user_document(request, draft_id)
            end_user_document = end_user_document.get('document')
        else:
            end_user_document = None

        for good in goods['goods']:
            if not good['good']['is_good_end_product']:
                ultimate_end_users_required = True

        context = {
            'title': 'Application Overview',
            'draft': data.get('draft'),
            'sites': sites['sites'],
            'goods': goods['goods'],
            'countries': countries['countries'],
            'goodstypes': goodstypes['goods'],
            'external_locations': external_locations['external_locations'],
            'ultimate_end_users': ultimate_end_users['ultimate_end_users'],
            'ultimate_end_users_required': ultimate_end_users_required,
            'end_user_document': end_user_document,
        }
        return render(request, 'apply_for_a_licence/overview.html', context)

    def post(self, request, **kwargs):
        draft_id = str(kwargs['pk'])
        data, status_code = submit_draft(request, draft_id)

        if status_code is not 201:
            draft, status_code = get_draft(request, draft_id)
            sites, status_code = get_sites_on_draft(request, draft_id)
            goods, status_code = get_draft_goods(request, draft_id)
            ultimate_end_users_required = False
            countries, status_code = get_draft_countries(request, draft_id)
            goodstypes, status_code = get_draft_goods_type(request, draft_id)
            external_locations, status_code = get_external_locations_on_draft(request, draft_id)
            ultimate_end_users, status_code = get_ultimate_end_users(request, draft_id)

            for good in goods['goods']:
                if not good['good']['is_good_end_product']:
                    ultimate_end_users_required = True

            context = {
                'title': 'Application Overview',
                'draft': draft.get('draft'),
                'errors': data.get('errors'),
                'sites': sites['sites'],
                'goods': goods['goods'],
                'countries': countries['countries'],
                'goodstypes': goodstypes['goods'],
                'external_locations': external_locations['external_locations'],
                'ultimate_end_users': ultimate_end_users['ultimate_end_users'],
                'ultimate_end_users_required': ultimate_end_users_required,
            }
            return render(request, 'apply_for_a_licence/overview.html', context)

        return success_page(request,
                            title='Application submitted',
                            secondary_title='',
                            description='',
                            what_happens_next=[],
                            links={'Go to applications': reverse_lazy('applications:applications')})


# Goods
class DraftGoodsList(TemplateView):
    def get(self, request, **kwargs):
        draft_id = str(kwargs['pk'])
        draft, status_code = get_draft(request, draft_id)
        data, status_code = get_draft_goods(request, draft_id)

        context = {
            'title': get_string('applications.standard.goods.title'),
            'draft_id': draft_id,
            'data': data,
            'draft': draft,
            'persistent_bar': create_persistent_bar(draft.get('draft')),
        }
        return render(request, 'apply_for_a_licence/goods/index.html', context)


class GoodsList(TemplateView):
    def get(self, request, **kwargs):
        draft_id = str(kwargs['pk'])
        draft, status_code = get_draft(request, draft_id)
        description = request.GET.get('description', '').strip()
        part_number = request.GET.get('part_number', '').strip()
        control_rating = request.GET.get('control_rating', '').strip()
        data, status_code = get_goods(request, {'description': description,
                                                'part_number': part_number,
                                                'control_rating': control_rating})

        filtered_data = []
        for good in data['goods']:
            if good['documents'] and not good['is_good_controlled'] == 'unsure':
                filtered_data.append(good)

        context = {
            'title': get_string('goods.add_from_organisation.title'),
            'draft_id': draft_id,
            'data': filtered_data,
            'draft': draft,
            'description': description,
            'part_number': part_number,
            'control_code': control_rating,
            'persistent_bar': create_persistent_bar(draft.get('draft')),
        }
        return render(request, 'apply_for_a_licence/goods/preexisting.html', context)


class DraftOpenGoodsList(TemplateView):
    def get(self, request, **kwargs):
        draft_id = str(kwargs['pk'])
        draft, status_code = get_draft(request, draft_id)
        data, status_code = get_draft_goods(request, draft_id)

        context = {
            'title': 'Application Goods',
            'draft_id': draft_id,
            'data': data,
            'draft': draft,
            'persistent_bar': create_persistent_bar(draft.get('draft')),
        }
        return render(request, 'apply_for_a_licence/goods/index.html', context)


class DraftOpenGoodsTypeList(TemplateView):
    def get(self, request, **kwargs):
        draft_id = str(kwargs['pk'])
        draft, status_code = get_draft(request, draft_id)
        data, status_code = get_draft_goods_type(request, draft_id)

        context = {
            'title': get_string('good_types.overview_good_types.title'),
            'draft_id': draft_id,
            'data': data,
            'draft': draft,
            'persistent_bar': create_persistent_bar(draft.get('draft')),
        }
        return render(request, 'apply_for_a_licence/goodstype/index.html', context)


class OpenGoodsList(TemplateView):
    def get(self, request, **kwargs):
        draft_id = str(kwargs['pk'])
        draft, status_code = get_draft(request, draft_id)
        description = request.GET.get('description', '')
        data, status_code = get_goods(request, {'description': description})

        context = {
            'title': 'Goods',
            'draft_id': draft_id,
            'data': data,
            'draft': draft,
            'description': description,
            'persistent_bar': create_persistent_bar(draft.get('draft')),
        }
        return render(request, 'apply_for_a_licence/goods/preexisting.html', context)


class AddPreexistingGood(TemplateView):
    def get(self, request, **kwargs):
        draft_id = str(kwargs['pk'])
        draft, status_code = get_draft(request, draft_id)
        good, status_code = get_good(request, str(kwargs['good_pk']))
        good = good.get('good')

        context = {
            'title': 'Add a pre-existing good to your application',
            'page': goods.preexisting_good_form(good.get('id'),
                                                good.get('description'),
                                                good.get('control_code'),
                                                good.get('part_number'),
                                                get_units(request)),
            'persistent_bar': create_persistent_bar(draft.get('draft')),
        }
        return render(request, 'form.html', context)

    def post(self, request, **kwargs):
        draft_id = str(kwargs['pk'])
        draft, status_code = get_draft(request, draft_id)
        data, status_code = post_draft_preexisting_goods(request, draft_id, request.POST)

        if status_code != 201:
            good, status_code = get_good(request, str(kwargs['good_pk']))
            good = good.get('good')

            context = {
                'title': 'Add a pre-existing good to your application',
                'page': goods.preexisting_good_form(good.get('id'),
                                                    good.get('description'),
                                                    good.get('control_code'),
                                                    good.get('part_number'),
                                                    get_units(request)),
                'persistent_bar': create_persistent_bar(draft.get('draft')),
                'data': request.POST,
                'errors': data.get('errors'),
            }
            return render(request, 'form.html', context)

        return redirect(reverse_lazy('apply_for_a_licence:goods', kwargs={'pk': draft_id}))


# Delete Application
class DeleteApplication(TemplateView):
    def get(self, request, **kwargs):
        draft_id = str(kwargs['pk'])
        draft, status_code = get_draft(request, draft_id)
        context = {
            'title': 'Are you sure you want to delete this application?',
            'draft': draft.get('draft'),
            'persistent_bar': create_persistent_bar(draft.get('draft')),
            'page': 'apply_for_a_licence/modals/cancel_application.html',
        }
        return render(request, 'core/static.html', context)

    def post(self, request, **kwargs):
        draft_id = str(kwargs['pk'])
        delete_draft(request, draft_id)

        if request.GET.get('return') == 'drafts':
            return redirect(reverse_lazy('drafts:index') + '/?application_deleted=true')

        return redirect('/?application_deleted=true')


# End User
class EndUser(TemplateView):
    def get(self, request, **kwargs):
        draft_id = str(kwargs['pk'])
        draft, status_code = get_draft(request, draft_id)

        return form_page(request, new_end_user_forms().forms[0], extra_data={
            'persistent_bar': create_persistent_bar(draft.get('draft'))
        })

    def post(self, request, **kwargs):
        draft_id = str(kwargs['pk'])
        response, data = submit_paged_form(request, new_end_user_forms(), post_end_user, pk=draft_id)

        # If there are more forms to go through, continue
        if response:
            return response

        draft, status_code = get_draft(request, draft_id)

        if draft.get('draft').get('licence_type').get('key') == STANDARD_LICENCE:
            return redirect(reverse_lazy('apply_for_a_licence:end_user_attach_document', kwargs={'pk': draft_id}))
        else:
            return redirect(reverse_lazy('apply_for_a_licence:overview', kwargs={'pk': draft_id}))


class UltimateEndUsers(TemplateView):
    def get(self, request, **kwargs):
        draft_id = str(kwargs['pk'])
        data, status_code = get_ultimate_end_users(request, draft_id)

        context = {
            'ultimate_end_users': data['ultimate_end_users'],
            'draft_id': draft_id,
            'title': 'Ultimate End Users',
            'description': get_string('ultimate_end_user.overview_description')
        }

        return render(request, 'apply_for_a_licence/ultimate_end_users/index.html', context)


class AddUltimateEndUser(TemplateView):
    draft_id = None
    form = None

    def dispatch(self, request, *args, **kwargs):
        self.draft_id = str(kwargs['pk'])
        self.form = new_ultimate_end_user_form()

        return super(AddUltimateEndUser, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        draft, status_code = get_draft(request, self.draft_id)

        return form_page(request, self.form.forms[0], extra_data={
            'persistent_bar': create_persistent_bar(draft.get('draft'))
        })

    def post(self, request, **kwargs):
        response, data = submit_paged_form(request, self.form, post_ultimate_end_user, pk=self.draft_id)

        if response:
            return response

        return redirect(reverse_lazy('apply_for_a_licence:ultimate_end_user_attach_document',
                                     kwargs={'pk': self.draft_id, 'ueu_pk': data['end_user']['id']}))


class RemoveUltimateEndUser(TemplateView):
    def get(self, request, **kwargs):
        draft_id = str(kwargs['pk'])
        ueu_pk = str(kwargs['ueu_pk'])
        delete_ultimate_end_user(request, draft_id, ueu_pk)
        data, status_code = get_ultimate_end_users(request, draft_id)

        context = {
            'ultimate_end_users': data['ultimate_end_users'],
            'draft_id': draft_id
        }

        return render(request, 'apply_for_a_licence/ultimate_end_users/index.html', context)


@method_decorator(csrf_exempt, 'dispatch')
class AttachDocuments(TemplateView):
    def get(self, request, **kwargs):
        draft_id = str(kwargs['pk'])
        draft, status_code = get_draft(request, draft_id)
        if status_code == 200:
            if draft.get('draft').get('licence_type').get('key') == STANDARD_LICENCE:
                if 'ultimate-end-user' in request.path:
                    back_text = get_string('ultimate_end_user.documents.attach_documents.back_to_application_overview')
                    draft_url = reverse('apply_for_a_licence:ultimate_end_users', kwargs={'pk': draft_id})
                    title = get_string('ultimate_end_user.documents.attach_documents.title')
                    return_later_text = get_string('ultimate_end_user.documents.save_end_user')
                else:
                    back_text = get_string('end_user.documents.attach_documents.back_to_application_overview')
                    draft_url = reverse('apply_for_a_licence:overview', kwargs={'pk': draft_id})
                    title = get_string('end_user.documents.attach_documents.title')
                    return_later_text = get_string('end_user.documents.save_end_user')

                form = attach_document_form(draft_url=draft_url, title=title,
                                            back_text=back_text, return_later_text=return_later_text)
                return form_page(request, form, extra_data={'draft_id': draft_id})
            else:
                return redirect(reverse_lazy('apply_for_a_licence:overview', kwargs={'pk': draft_id}))
        else:
            return error_page(None, 'Cannot find draft')

    @csrf_exempt
    def post(self, request, **kwargs):
        self.request.upload_handlers.insert(0, S3FileUploadHandler(request))
        logging.info(self.request)
        draft_id = str(kwargs['pk'])
        data, error = add_document_data(request)

        if error:
            return error_page(None, get_string('end_user.documents.attach_documents.upload_error'))

        # Send LITE API the file information
        if 'ultimate-end-user' in request.path:
            end_user_document, status_code = post_ultimate_end_user_document(request, draft_id,
                                                                             str(kwargs['ueu_pk']), data)
            next_page = 'apply_for_a_licence:ultimate_end_users'
        else:
            end_user_document, status_code = post_end_user_document(request, draft_id, data)
            next_page = 'apply_for_a_licence:overview'

        if status_code != 201:
            return error_page(None, get_string('end_user.documents.attach_documents.upload_error'))
        return redirect(reverse(next_page, kwargs={'pk': draft_id}))


class DownloadDocument(TemplateView):
    def get(self, request, **kwargs):
        draft_id = str(kwargs['pk'])

        if 'ultimate-end-user' in request.path:
            document, status_code = get_ultimate_end_user_document(request, draft_id, str(kwargs['ueu_pk']))
        else:
            document, status_code = get_end_user_document(request, draft_id)

        document = document['document']

        if document['safe']:
            return download_document_from_s3(document['s3_key'], document['name'])
        else:
            return error_page(None, get_string('end_user.documents.attach_documents.download_error'))


class DeleteDocument(TemplateView):
    def get(self, request, **kwargs):
        if 'ultimate-end-user' in request.path:
            back_address = 'apply_for_a_licence:ultimate_end_users'
            back_link_text = get_string('ultimate_end_user.documents.attach_documents.back_to_application_overview')
        else:
            back_address = 'apply_for_a_licence:overview'
            back_link_text = get_string('end_user.documents.attach_documents.back_to_application_overview')
        form = delete_document_confirmation_form(
            overview_url=reverse(back_address, kwargs={'pk': str(kwargs['pk'])}),
            back_link_text=back_link_text
        )

        return form_page(request, form)

    def post(self, request, **kwargs):
        draft_id = str(kwargs['pk'])
        option = request.POST.get('delete_document_confirmation')
        if option is None:
            return redirect(request.path_info, kwargs={'pk': draft_id})
        elif option == 'yes':
            if 'ultimate-end-user' in request.path:
                status_code = delete_ultimate_end_user_document(request, draft_id, str(kwargs['ueu_pk']))
            else:
                status_code = delete_end_user_document(request, draft_id)
            if status_code is not 204:
                return error_page(None, get_string('end_user.documents.attach_documents.delete_error'))

        if 'ultimate-end-user' in request.path:
            return redirect(reverse('apply_for_a_licence:ultimate_end_users', kwargs={'pk': str(kwargs['pk'])}))
        else:
            return redirect(reverse('apply_for_a_licence:overview', kwargs={'pk': draft_id}))

