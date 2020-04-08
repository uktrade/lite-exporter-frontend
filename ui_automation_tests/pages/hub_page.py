from ui_automation_tests.shared.BasePage import BasePage


class Hub(BasePage):

    SWITCH_LINK = "switch-link"  # ID
    SITES_BTN = "[href*='/sites/']"  # CSS
    APPLICATION_BTN = "a[href*='/applications/']"  # CSS
    TILE_APPLICATIONS_ID = "applications-notifications"  # ID

    def click_applications(self):
        self.driver.find_element_by_css_selector(self.APPLICATION_BTN).click()

    def click_sites_link(self):
        self.driver.find_element_by_css_selector(self.SITES_BTN).click()

    def click_switch_link(self):
        self.driver.find_element_by_id(self.SWITCH_LINK).click()

    def get_text_of_application_tile(self):
        return self.driver.find_element_by_id(self.TILE_APPLICATIONS_ID).text

    def return_number_of_notifications(self):
        text_of_new_notifications = self.driver.find_element_by_id(self.TILE_APPLICATIONS_ID).text
        return int(text_of_new_notifications)
