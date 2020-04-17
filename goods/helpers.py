from django.utils.safestring import mark_safe

from applications.helpers.date_fields import format_date
from core.builtins.custom_tags import default_na
from core.helpers import convert_control_list_entries
from lite_forms.components import Summary


def good_summary(good):
    if not good:
        return

    return Summary(
        values={
            "Description": good["description"],
            "Control list entries": convert_control_list_entries(good["control_list_entries"]),
            "Part number": default_na(good["part_number"]),
        },
        classes=["govuk-summary-list--no-border"],
    )


def process_pv_grading_for_post(json):
    json = {
        "is_pv_graded": json["is_pv_graded"],
        "pv_grading_details": {
            "grading": json["grading"],
            "custom_grading": json["custom_grading"],
            "prefix": json["prefix"],
            "suffix": json["suffix"],
            "issuing_authority": json["issuing_authority"],
            "reference": json["reference"],
            "date_of_issue": format_date(json, "date_of_issue"),
        }
    }

    return json
