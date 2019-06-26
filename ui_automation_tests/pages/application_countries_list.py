class ApplicationCountriesList:

    def __init__(self, driver):
        self.driver = driver
        self.countries_checkboxes = ".govuk-checkboxes__input"

    def select_countries(self):
        self.driver.find_elements_by_css_selector(self.countries_checkboxes)[0].click()
