from munch import Munch

from conf.constants import APPLICANT_EDITING
from core.builtins.custom_tags import str_date


class Application(Munch):
    @property
    def type_reference(self):
        return getattr(self, "case_type")["reference"]["key"]

    @property
    def type_reference_value(self):
        return getattr(self, "case_type")["reference"]["value"]

    @property
    def sub_type(self):
        return getattr(self, "case_type")["sub_type"]["key"]

    @property
    def sub_type_value(self):
        return getattr(self, "case_type")["sub_type"]["value"]

    @property
    def status(self):
        # Status can sometime be null, hence use a get
        return getattr(self, "status").get("key")

    @property
    def created_at(self):
        return str_date(getattr(self, "created_at"))

    @property
    def submitted_at(self):
        return str_date(getattr(self, "submitted_at"))

    def is_editable(self):
        if self.status:
            is_editing = self.status == "submitted" or self.status == APPLICANT_EDITING
            if is_editing:
                return self.status == "submitted"

    def is_major_editable(self):
        if self.status:
            is_editing = self.status == "submitted" or self.status == APPLICANT_EDITING
            if is_editing:
                return self.status != "submitted"
