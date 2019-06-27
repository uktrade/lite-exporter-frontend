class ApplicationCountriesList:

    def __init__(self, driver):
        self.driver = driver
        self.countries_checkboxes = ".govuk-checkboxes__input"
        self.countries_labels = ".govuk-checkboxes__label"

    def get_countries_names(self):
        countries_names = []
        for country in self.driver.find_elements_by_css_selector(self.countries_labels):
            countries_names.append(country.text)
        return countries_names

    def view_countries(self):
        for checkbox in self.driver.find_elements_by_css_selector(self.countries_checkboxes):
            checkbox.click()

    def select_country(self, name):
        checkbox = self.driver.find_element_by_id(name)
        checkbox.click()
