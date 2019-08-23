class Shared:

    def __init__(self, driver):
        self.driver = driver
        self.submit_button = "button[type*='submit']"
        self.back_link = ".govuk-back-link"
        self.error_messages = ".govuk-error-summary__body"

    def get_text_of_error_messages(self):
        return self.driver.find_element_by_css_selector(self.error_messages).text

    def click_continue(self):
        self.driver.find_element_by_css_selector(self.submit_button).click()

    def click_back_link(self):
        self.driver.find_element_by_css_selector(self.back_link).click()

    def is_error_message_displayed(self):
        return self.driver.find_element_by_css_selector(self.error_messages).is_displayed()

    def get_text_of_body(self):
        return self.driver.find_element_by_tag_name("body").text

