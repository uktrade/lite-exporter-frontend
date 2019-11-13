from core.builtins.custom_tags import str_date
from lite_forms.components import Summary


def application_summary(application):
    if not application:
        return

    return Summary(
        values={
            'Reference': application['name'],
            'Licence type': application['licence_type']['value'],
            'Export type': application['export_type']['value'],
            'Submitted at': str_date(application['submitted_at'])
        },
        classes=['govuk-summary-list--no-border'])
