from conf.constants import APPLICANT_EDITING


class ApplicationEditTypes:
    MINOR_EDIT = "minor_edit"
    MAJOR_EDIT = "major_edit"


def get_application_edit_type(application: dict):
    """
    TODO
    """
    if application["status"]:
        is_editing = application["status"]["key"] == "submitted" or application["status"]["key"] == APPLICANT_EDITING
        if is_editing:
            return (
                ApplicationEditTypes.MINOR_EDIT
                if application["status"]["key"] == "submitted"
                else ApplicationEditTypes.MAJOR_EDIT
            )
    return None
