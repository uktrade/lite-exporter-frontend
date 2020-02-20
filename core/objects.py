from munch import Munch


class Application(Munch):
    def get_application_type_reference(self):
        return getattr(self, "case_type")["reference"]["key"]

    def get_application_sub_type(self):
        return getattr(self, "case_type")["sub_type"]["key"]

    def get_status(self):
        return getattr(self, "status")["key"]
