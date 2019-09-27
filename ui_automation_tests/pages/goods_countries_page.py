class GoodsCountriesPage:
    def __init__(self, driver):
        self.driver = driver

    def select_all(self):
        elements = self.driver.find_elements_by_css_selector(".govuk-checkboxes__input")
        for element in elements:
            if not element.is_selected():
                element.click()

    def deselect_all(self):
        elements = self.driver.find_elements_by_css_selector(".govuk-checkboxes__input")
        for element in elements:
            if element.is_selected():
                element.click()

    def all_selected(self):
        elements = self.driver.find_elements_by_css_selector(".govuk-checkboxes__input")
        for element in elements:
            if not element.is_selected():
                return False

        return True

    def all_deselected(self):
        elements = self.driver.find_elements_by_css_selector(".govuk-checkboxes__input")
        for element in elements:
            if element.is_selected():
                return False

        return True
