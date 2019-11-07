from selenium.webdriver.common.keys import Keys


class HMRCQueryPage:

    def __init__(self, driver):
        self.driver = driver

        self.govuk_input = '.govuk-input'
        self.org_radio_gutton_id_part = 'organisation-'
        self.continue_button = "button[value='continue']"

    def search_for_org(self, name):
        input = self.driver.find_element_by_css_selector(self.govuk_input)
        input.clear()
        input.send_keys(name)
        input.send_keys(Keys.ENTER)

    def click_org_radio_button(self, org_id):
        self.driver.find_element_by_id(self.org_radio_gutton_id_part + org_id).click()

    def click_continue(self):
        self.driver.find_element_by_css_selector(self.continue_button).click()
