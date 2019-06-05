class WhichLocationFormPage():

    def __init__(self, driver):
        self.driver = driver
        self.at_my_sites_radio_button = "organisation_or_external-organisation" #id
        self.external_location_radio_button = "organisation_or_external-external" #id

    def click_on_my_sites_radio_button(self):
        self.driver.find_element_by_css_selector(self.at_my_sites_radio_button).click()

    def click_on_external_location_radio_button(self):
        self.driver.find_element_by_css_selector(self.external_location_radio_button).click()
