from munch import Munch

from conf.constants import APPLICANT_EDITING
from core.builtins.custom_tags import str_date


class Application(Munch):
    def get_application_type_reference(self):
        return getattr(self, "case_type")["reference"]["key"]

    def get_application_type_reference_value(self):
        return getattr(self, "case_type")["reference"]["value"]

    def get_application_sub_type(self):
        return getattr(self, "case_type")["sub_type"]["key"]

    def get_application_sub_type_value(self):
        return getattr(self, "case_type")["sub_type"]["value"]

    def get_status(self):
        # Status can sometime be null, hence use a get
        return getattr(self, "status").get("key")

    def get_created_at(self):
        return str_date(getattr(self, "created_at"))

    def get_submitted_at(self):
        return str_date(getattr(self, "submitted_at"))

    def is_editable(self):
        status = self.get_status()

        if status:
            is_editing = status == "submitted" or status == APPLICANT_EDITING
            if is_editing:
                return status == "submitted"

    def is_major_editable(self):
        status = self.get_status()

        if status:
            is_editing = status == "submitted" or status == APPLICANT_EDITING
            if is_editing:
                return status != "submitted"
