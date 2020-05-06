from django.shortcuts import render

from applications.constants import OielLicenceTypes
from applications.helpers.check_your_answers import _is_application_export_type_temporary
from applications.helpers.task_list_sections import (
    get_reference_number_description,
    get_edit_type,
    get_end_use_details,
    get_route_of_goods,
    get_temporary_export_details,
)
from applications.services import (
    get_application_countries,
    get_application_goods,
    get_additional_documents,
)
from conf.constants import (
    HMRC,
    OPEN,
    STANDARD,
    EXHIBITION,
    F680,
    GIFTING,
    Permissions,
)
from core.services import get_sites_on_draft, get_external_locations_on_draft
from lite_content.lite_exporter_frontend.strings import applications
from organisation.roles.services import get_user_permissions


def _get_strings(application_type):
    if application_type == STANDARD:
        return applications.StandardApplicationTaskList
    elif application_type == OPEN:
        return applications.OpenApplicationTaskList
    elif application_type == HMRC:
        return applications.HMRCApplicationTaskList
    elif application_type == EXHIBITION:
        return applications.ExhibitionClearanceTaskList
    elif application_type == F680:
        return applications.F680ClearanceTaskList
    elif application_type == GIFTING:
        return applications.GiftingClearanceTaskList
    elif application_type == HMRC:
        return applications.HMRCApplicationTaskList
    else:
        raise NotImplementedError(f"No string class for given for {application_type}")


def get_application_task_list(request, application, errors=None):
    user_permissions = get_user_permissions(request)
    additional_documents, _ = get_additional_documents(request, application["id"])
    sites, _ = get_sites_on_draft(request, application["id"])
    external_locations, _ = get_external_locations_on_draft(request, application["id"])
    application_type = application.sub_type
    is_editing, edit_type = get_edit_type(application)

    context = {
        "strings": _get_strings(application_type),
        "application": application,
        "application_type": application_type,
        "is_editing": is_editing,
        "edit_type": edit_type,
        "errors": errors,
    }

    if application_type == HMRC:
        context["locations"] = application["goods_locations"] or application["have_goods_departed"]
        return render(request, "applications/hmrc-application.html", context)

    context["can_submit"] = Permissions.SUBMIT_LICENCE_APPLICATION in user_permissions
    context["supporting_documents"] = additional_documents["documents"]
    context["locations"] = sites["sites"] or external_locations["external_locations"]

    if application_type == F680:
        context["end_use_details"] = get_end_use_details(application)
    elif application_type == STANDARD:
        context["reference_number_description"] = get_reference_number_description(application)
        context["end_use_details"] = get_end_use_details(application)
        context["route_of_goods"] = get_route_of_goods(application)
        if _is_application_export_type_temporary(application):
            context["temporary_export_details"] = get_temporary_export_details(application)
    elif application_type == OPEN:
        context["countries"] = get_application_countries(request, application["id"])
        context["end_use_details"] = get_end_use_details(application)
        context["goodstypes"] = application["goods_types"]
        if _is_application_export_type_temporary(application):
            context["temporary_export_details"] = get_temporary_export_details(application)
        goods_types = application.get("goods_types")
        if goods_types:
            destination_countries = [goods_type["countries"] for goods_type in goods_types][0]
            context["destinations"] = set([destination["id"] for destination in destination_countries])
            if application["goodstype_category"]["key"] == "military":
                context["ultimate_end_users_required"] = True in [
                    goods_type["is_good_incorporated"] for goods_type in goods_types
                ]
        context["route_of_goods"] = get_route_of_goods(application)

        if application.get("goodstype_category"):
            goodstype_category = application.get("goodstype_category").get("key")
            context["is_crypto_application"] = goodstype_category == "cryptographic"
            context["oiel_noneditable_countries"] = OielLicenceTypes.is_non_editable_country(goodstype_category)

    if not application_type == OPEN:
        context["goods"] = get_application_goods(request, application["id"])
        context["ultimate_end_users_required"] = True in [good["is_good_incorporated"] for good in context["goods"]]

    return render(request, "applications/task-list.html", context)
