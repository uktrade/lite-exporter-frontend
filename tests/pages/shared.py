class Shared():

    def __init__(self, driver):
        self.driver = driver
        self.submit_button = driver.find_element_by_css_selector("button[type*='submit']")
        self.error_message = driver.find_element_by_css_selector(".govuk-error-message")

    def click_save_and_continue(self):
        self.self.submit_button.click()

    def get_text_of_error_message(self):
        return self.driver.find_element_by_css_selector(".govuk-error-message").text

    def is_error_message_displayed(self):
        return self.driver.find_element_by_css_selector(".govuk-error-message").is_displayed()

    def get_text_of_error_message_at_position_2(self):
        return self.driver.find_elements_by_css_selector(".govuk-error-message")[1].text

