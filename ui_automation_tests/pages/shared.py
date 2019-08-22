class Shared:

    def __init__(self, driver):
        self.driver = driver
        self.submit_button = "button[type*='submit']"
        self.back_link = ".govuk-back-link"
        self.error_messages = ".govuk-error-summary__body"
        self.confirm_yes = '.govuk-radios__input[value="yes"]'
        self.confirm_no = '.govuk-radios__input[value="yes"]'

    def get_text_of_error_messages(self):
        return self.driver.find_element_by_css_selector(self.error_messages).text

    def click_continue(self):
        self.driver.find_element_by_css_selector(self.submit_button).click()

    def click_back_link(self):
        self.driver.find_element_by_css_selector(self.back_link).click()

    def click_confirm_yes(self):
        self.driver.find_element_by_css_selector(self.confirm_yes).click()

    def click_confirm_no(self):
        self.driver.find_element_by_css_selector(self.confirm_no).click()

    def is_error_message_displayed(self):
        return self.driver.find_element_by_css_selector(self.error_messages).is_displayed()

    def get_text_of_body(self):
        return self.driver.find_element_by_tag_name("body").text

