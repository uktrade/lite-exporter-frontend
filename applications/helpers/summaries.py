from lite_content.lite_exporter_frontend import strings
from lite_forms.components import Summary


def draft_summary(draft):
    if not draft:
        return None

    return Summary(
        values={
            strings.applications.ApplicationSummaryPage.REFERENCE_NAME: draft["name"],
            strings.applications.ApplicationSummaryPage.TYPE: draft.get_application_sub_type_value(),
            strings.applications.ApplicationSummaryPage.CREATED_AT: draft.get_created_at(),
        },
        classes=["govuk-summary-list--no-border"],
    )


def application_summary(application):
    if not application:
        return None

    return Summary(
        values={
            strings.applications.ApplicationSummaryPage.REFERENCE_NAME: application["name"],
            strings.applications.ApplicationSummaryPage.REFERENCE_CODE: application["reference_code"],
            strings.applications.ApplicationSummaryPage.TYPE: application.get_application_sub_type_value(),
            strings.applications.ApplicationSummaryPage.SUBMITTED_AT: application.get_submitted_at(),
        },
        classes=["govuk-summary-list--no-border"],
    )
