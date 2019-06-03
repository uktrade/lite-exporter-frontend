class SitesPage():

    def __init__(self, driver):
        self.driver = driver
        self.sites_checkbox = ".govuk-checkboxes__input"


    def click_sites_checkbox(self):
        self.driver.find_element_by_css_selector(self.sites_checkbox).click()
