from django.shortcuts import render

from applications.services import get_additional_documents, get_ultimate_end_users, get_third_parties, \
    get_application_goods, get_end_user_document, get_consignee_document, get_application_countries, \
    get_application_goods_types
from apply_for_a_licence.views import check_all_parties_have_a_document
from conf.constants import STANDARD_LICENCE
from core.services import get_sites_on_draft, get_external_locations_on_draft


def get_licence_overview(request, application, errors=None):
    application_id = application['id']

    sites, _ = get_sites_on_draft(request, application_id)
    external_locations, _ = get_external_locations_on_draft(request, application_id)
    additional_documents, _ = get_additional_documents(request, application_id)

    countries = {'countries': []}
    goods = {'goods': []}
    goodstypes = {'goods': []}
    ultimate_end_users = {'ultimate_end_users': []}
    ultimate_end_users_required = False
    third_parties = {'third_parties': []}
    end_user_document = None
    consignee_document = None
    countries_on_goods_types = False

    if application['licence_type']['key'] == STANDARD_LICENCE:
        ultimate_end_users, _ = get_ultimate_end_users(request, application_id)
        third_parties, _ = get_third_parties(request, application_id)
        end_user = application.get('end_user')
        consignee = application.get('consignee')
        goods = get_application_goods(request, application_id)

        if end_user:
            end_user_document, _ = get_end_user_document(request, application_id)
            end_user_document = end_user_document.get('document')

        if consignee:
            consignee_document, _ = get_consignee_document(request, application_id)
            consignee_document = consignee_document.get('document')

        for good in goods:
            if not good['good']['is_good_end_product']:
                ultimate_end_users_required = True
    else:
        goodstypes = get_application_goods_types(request, application_id)
        countries, _ = get_application_countries(request, application_id)

        for good in goodstypes:
            if good['countries']:
                countries_on_goods_types = True

    context = {
        'application': application,
        'sites': sites['sites'],
        'goods': goods,
        'countries': countries['countries'],
        'goodstypes': goodstypes,
        'external_locations': external_locations['external_locations'],
        'ultimate_end_users': ultimate_end_users['ultimate_end_users'],
        'ultimate_end_users_required': ultimate_end_users_required,
        'ultimate_end_users_documents_complete':
            check_all_parties_have_a_document(ultimate_end_users['ultimate_end_users']),
        'end_user_document': end_user_document,
        'consignee_document': consignee_document,
        'countries_on_goods_types': countries_on_goods_types,
        'third_parties': third_parties['third_parties'],
        'additional_documents': additional_documents['documents']
    }

    if errors:
        context['errors'] = errors

    return render(request, 'apply_for_a_licence/overview.html', context)
