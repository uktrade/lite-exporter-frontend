class Shared:

    def __init__(self, driver):
        self.driver = driver
        self.submit_button = "button[type*='submit']"
        self.error_message = ".govuk-error-message"
        self.gov_body = ".govuk-error-message"
        self.gov_table_cell_links = "..govuk-table__cell a"

    def get_text_of_error_message(self, position=0):
        return self.driver.find_elements_by_css_selector(self.error_message)[position].text

    def click_continue(self):
        self.driver.find_element_by_css_selector(self.submit_button).click()

    def is_error_message_displayed(self):
        return self.driver.find_element_by_css_selector(self.error_message).is_displayed()

    def get_text_of_body(self):
        return self.driver.find_element_by_tag_name("body").text

    def get_text_of_gov_body(self):
        return self.driver.find_element_by_css_selector(self.gov_body).text

    def get_gov_table_cell_links(self):
        return self.driver.find_elements_by_css_selector(self.gov_table_cell_links)

