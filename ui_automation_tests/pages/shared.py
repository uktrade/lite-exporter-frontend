class Shared:

    def __init__(self, driver):
        self.driver = driver
        self.submit_button = "button[type*='submit']"
        self.error_message = ".govuk-error-message"
        self.gov_uk_table_row = ".govuk-table__row"
        self.gov_uk_table = ".govuk-table"

    def get_text_of_error_message(self, position=0):
        return self.driver.find_elements_by_css_selector(self.error_message)[position].text

    def click_continue(self):
        self.driver.find_element_by_css_selector(self.submit_button).click()

    def is_error_message_displayed(self):
        return self.driver.find_element_by_css_selector(self.error_message).is_displayed()

    def get_text_of_body(self):
        return self.driver.find_element_by_tag_name("body").text

    def get_text_of_gov_table(self):
        return self.driver.find_element_by_css_selector(self.gov_uk_table).text

    def get_table_rows(self):
        return self.driver.find_elements_by_css_selector(self.gov_uk_table_row)