class Shared:

    def __init__(self, driver):
        self.driver = driver
        self.submit_button = "button[type*='submit']"  # CSS
        self.error_message = ".govuk-error-message"  # CSS
        self.gov_uk_table_row = ".govuk-table__row"  # CSS
        self.gov_uk_table = ".govuk-table"  # CSS
        self.heading = ".govuk-heading-xl"  # CSS
        self.radio_buttons = ".govuk-radios__input"  # CSS

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

    def get_text_of_heading(self):
        return self.driver.find_element_by_css_selector(self.heading).text

    def click_on_radio_buttons(self, no):
        return self.driver.find_elements_by_css_selector(self.radio_buttons)[no].click()
