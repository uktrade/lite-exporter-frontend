from shared.BasePage import BasePage
from shared import functions


class AddEndUserPages(BasePage):
    NAME_FIELD = "name"  # ID
    ADDRESS_FIELD = "address"  # ID
    COUNTRY_FIELD = "country"  # ID
    WEBSITE_FIELD = "website"  # ID

    FILTER_LINK = "show-filters-link"  # ID
    FILTER_NAME_FIELD = "name"  # ID
    FILTER_ADDRESS_FIELD = "address"  # ID
    FILTER_COUNTRY_FIELD = "country"  # ID
    FILTER_BUTTON = "button-apply-filters"  # ID

    ADD_NEW_ADDRESS_BUTTON = 'a[href*="add"]'
    TYPE_CHOICES = "sub_type-"
    CREATE_NEW_CONFIRMATION = "copy_existing"  # ID
    COPY_EXISTING_BUTTON = "add"  # Name

    def create_new_or_copy_existing(self, copy_existing: bool):
        if copy_existing:
            self.driver.find_element_by_id(f"{self.CREATE_NEW_CONFIRMATION}-yes").click()
        else:
            self.driver.find_element_by_id(f"{self.CREATE_NEW_CONFIRMATION}-no").click()
        functions.click_submit(self.driver)

    def enter_name(self, name):
        name_tb = self.driver.find_element_by_id(self.NAME_FIELD)
        name_tb.clear()
        name_tb.send_keys(name)

    def get_name(self):
        return self.driver.find_element_by_id(self.NAME_FIELD).get_attribute("value")

    def enter_address(self, address):
        address_tb = self.driver.find_element_by_id(self.ADDRESS_FIELD)
        address_tb.clear()
        address_tb.send_keys(address)

    def get_address(self):
        return self.driver.find_element_by_id(self.ADDRESS_FIELD).get_attribute("value")

    def enter_website(self, website):
        address_tb = self.driver.find_element_by_id(self.WEBSITE_FIELD)
        address_tb.clear()
        address_tb.send_keys(website)

    def get_website(self):
        return self.driver.find_element_by_id(self.WEBSITE_FIELD).get_attribute("value")

    def enter_country(self, country):
        country_tb = self.driver.find_element_by_id(self.COUNTRY_FIELD)
        country_tb.send_keys(country)

    def get_country(self):
        return self.driver.find_element_by_id(self.COUNTRY_FIELD).get_attribute("value")

    def select_type(self, string):
        self.driver.find_element_by_id(self.TYPE_CHOICES + string).click()

    def click_copy_existing_button(self):
        self.driver.find_element_by_name(self.COPY_EXISTING_BUTTON).click()

    def open_parties_filter(self):
        self.driver.find_element_by_id(self.FILTER_LINK).click()

    def filter_name(self, text):
        self.driver.find_element_by_id(self.FILTER_NAME_FIELD).send_keys(text)

    def filter_address(self, text):
        self.driver.find_element_by_id(self.FILTER_ADDRESS_FIELD).send_keys(text)

    def filter_country(self, text):
        self.driver.find_element_by_id(self.FILTER_COUNTRY_FIELD).send_keys(text)

    def submit_filter(self):
        self.driver.find_element_by_id(self.FILTER_BUTTON).click()
