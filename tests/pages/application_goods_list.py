from selenium.webdriver.support.ui import Select


class ApplicationGoodsList():

    def __init__(self, driver):
        self.driver = driver
        self.add_from_org_goods_button = 'a.govuk-button[href*="add_preexisting"]'
        self.add_to_application = driver.find_elements_by_css_selector('a.govuk-button')
        self.overview_link = '.govuk-back-link'
        self.quantity_field = 'quantity'
        self.unit_dropdown = 'unit'
        self.value_field = 'value'


    def click_add_from_organisations_goods_button(self):
        return self.driver.find_element_by_css_xselector('a.govuk-button[href*="add_preexisting"]').click()

    def click_add_to_application(self, no):
        return self.add_to_application[no-1].click()

    def add_values_to_good(self, value, quantity, unit):
        self.driver.find_element_by_id(self.value_field).send_keys(value)
        self.driver.find_element_by_id(self.quantity_field).send_keys(quantity)
        select = Select(self.driver.find_element_by_id(self.unit_dropdown))
        select.select_by_visible_text(unit)

    def click_on_overview(self):
        self.driver.find_element_by_css_selector(self.overview_link).click()
