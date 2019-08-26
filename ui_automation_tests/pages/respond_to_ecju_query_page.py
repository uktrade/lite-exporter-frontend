from selenium.webdriver.common.keys import Keys


class RespondToEcjuQueryPage:

    def __init__(self, driver):
        self.driver = driver
        self.response_form = 'response'  # id
        self.submit_button = "button[type*='submit']"

    def enter_form_response(self, value):
        address_tb = self.driver.find_element_by_id(self.response_form)
        address_tb.clear()
        address_tb.send_keys(value)

    def click_submit(self):
        self.driver.find_element_by_css_selector(self.submit_button).click()
