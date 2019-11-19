import logging

from shared import functions
from shared.BasePage import BasePage

log = logging.getLogger()
console = logging.StreamHandler()
log.addHandler(console)


class ApplyForALicencePage(BasePage):

    name_or_reference_input_id = "name"
    BUTTON_STANDARD_LICENCE = "input#application_type-standard_licence"
    BUTTON_OPEN_LICENCE = "input#application_type-open_licence"
    export_button = "export_type-"
    export_licence_yes_or_no = "have_you_been_informed-"
    reference_number = "reference_number_on_information_form"
    success_message = ".govuk-panel__title"
    application_is_submitted = ".govuk-panel__title"
    LINK_DELETE_DRAFT_ID = "link-delete-draft"

    def enter_name_or_reference_for_application(self, name):
        element = self.driver.find_element_by_id(self.name_or_reference_input_id)
        element.clear()
        element.send_keys(name)

    def click_delete_application(self):
        self.driver.find_element_by_id(self.LINK_DELETE_DRAFT_ID).click()
        self.driver.find_element_by_id("choice-yes").click()
        functions.click_submit(self.driver)

    def click_export_licence(self, export_type):
        logging.info(export_type)
        if export_type == "standard":
            return self.driver.find_element_by_css_selector(self.BUTTON_STANDARD_LICENCE).click()
        elif export_type == "open":
            return self.driver.find_element_by_css_selector(self.BUTTON_OPEN_LICENCE).click()

    def click_permanent_or_temporary_button(self, string):
        self.driver.find_element_by_id(self.export_button + string).click()

    def click_export_licence_yes_or_no(self, string):
        self.driver.find_element_by_id(self.export_licence_yes_or_no + string).click()

    def get_text_of_success_message(self):
        return self.driver.find_element_by_css_selector(self.success_message).text

    def type_into_reference_number(self, string):
        self.driver.find_element_by_id(self.reference_number).clear()
        self.driver.find_element_by_id(self.reference_number).send_keys(string)

    def application_submitted_text(self):
        return self.driver.find_element_by_css_selector(self.application_is_submitted).text
