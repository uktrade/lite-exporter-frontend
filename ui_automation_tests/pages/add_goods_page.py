from selenium.webdriver.support.select import Select


class AddGoodPage:
    DOCUMENT_VALID_YES = "has_document_to_upload-yes"  # ID
    DOCUMENT_VALID_NO = "has_document_to_upload-no"  # ID
    ECJU_HELPLINE = "ecju_contact"  # ID
    MISSING_DOCUMENT_REASON = "missing_document_reason"  # ID
    GOOD_SUMMARY = ".govuk-summary-list"  # CSS

    def __init__(self, driver, prefix=""):
        self.driver = driver
        self.add_a_good_btn = "#add-a-good"
        self.prefix = prefix

    def click_add_a_good(self):
        self.driver.find_element_by_css_selector(self.add_a_good_btn).click()

    def enter_description_of_goods(self, description):
        description_tb = self.driver.find_element_by_id(self.prefix + "description")
        description_tb.clear()
        description_tb.send_keys(description)

    def select_is_your_good_controlled(self, option):
        # The only options accepted here are 'yes', 'no' and 'unsure'
        self.driver.find_element_by_id(self.prefix + "is_good_controlled-%s" % option.lower()).click()

    def enter_control_code(self, code):
        control_code_tb = self.driver.find_element_by_id(self.prefix + "control_code")
        control_code_tb.clear()
        control_code_tb.send_keys(code)

        # This is done as control code textbox needs to lose focus
        self.driver.find_element_by_tag_name("body").click()

    def enter_control_code_unsure(self, code):
        control_code_tb = self.driver.find_element_by_id(self.prefix + "not_sure_details_control_code")
        control_code_tb.clear()
        control_code_tb.send_keys(code)

    def enter_control_unsure_details(self, details):
        unsure_details = self.driver.find_element_by_id(self.prefix + "not_sure_details_details")
        unsure_details.clear()
        unsure_details.send_keys(details)

    def select_control_unsure_confirmation(self, option):
        # The only options accepted here are 'yes' and 'no
        self.driver.find_element_by_id(self.prefix + "clc_query_confirmation-" + option.lower()).click()

    def select_is_your_good_intended_to_be_incorporated_into_an_end_product(self, option):
        if option == "Yes":
            self.driver.find_element_by_id(self.prefix + "is_good_end_product-no").click()
        else:
            self.driver.find_element_by_id(self.prefix + "is_good_end_product-yes").click()

    def enter_part_number(self, part_number):
        part_number_tb = self.driver.find_element_by_id(self.prefix + "part_number")
        part_number_tb.clear()
        part_number_tb.send_keys(part_number)

    def confirm_can_upload_good_document(self):
        self.driver.find_element_by_id(self.DOCUMENT_VALID_YES).click()

    def confirm_cannot_upload_good_document(self):
        self.driver.find_element_by_id(self.DOCUMENT_VALID_NO).click()

    def get_ecju_help(self):
        return self.driver.find_element_by_id(self.ECJU_HELPLINE).is_displayed()

    def select_valid_missing_document_reason(self):
        Select(self.driver.find_element_by_id(self.MISSING_DOCUMENT_REASON)).select_by_index(1)

    def get_good_summary_text(self):
        return self.driver.find_element_by_css_selector(self.GOOD_SUMMARY).text
