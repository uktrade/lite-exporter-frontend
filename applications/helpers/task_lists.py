from django.shortcuts import render

from applications.helpers.task_list_sections import (
    get_reference_number_description,
    get_edit_type,
)
from applications.services import (
    get_application_countries,
    get_application_goods_types,
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
from roles.services import get_user_permissions


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
    application_type = application["case_type"]["sub_type"]["key"]
    edit = get_edit_type(application)

    context = {
        "strings": _get_strings(application_type),
        "application": application,
        "application_type": application_type,
        "is_editing": edit[0],
        "edit_type": edit[1],
        "errors": errors,
    }

    if application_type != HMRC:
        context["can_submit"] = Permissions.SUBMIT_LICENCE_APPLICATION in user_permissions
        context["supporting_documents"] = additional_documents["documents"]
        context["locations"] = sites["sites"] or external_locations["external_locations"]

        if application_type == STANDARD:
            context["reference_number_description"] = get_reference_number_description(application)

        if application_type == OPEN:
            context["countries"] = get_application_countries(request, application["id"])
            context["goodstypes"] = get_application_goods_types(request, application["id"])
        else:
            context["goods"] = get_application_goods(request, application["id"])
            context["ultimate_end_users_required"] = True in [good["is_good_incorporated"] for good in context["goods"]]

        return render(request, "applications/task-list.html", context)

    else:
        context["locations"] = application["goods_locations"] or application["have_goods_departed"]
        return render(request, "applications/hmrc-application.html", context)
