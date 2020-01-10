from shared.BasePage import BasePage
from shared import functions


class AddEndUserPages(BasePage):
    INPUT_NAME_ID = "name"  # ID
    INPUT_ADDRESS_ID = "address"  # ID
    INPUT_COUNTRY_ID = "country"  # ID
    INPUT_WEBSITE_ID = "website"  # ID

    FILTER_LINK = "show-filters-link"  # ID
    FILTER_NAME_FIELD = "name"  # ID
    FILTER_ADDRESS_FIELD = "address"  # ID
    FILTER_COUNTRY_FIELD = "country"  # ID
    FILTER_BUTTON = "button-apply-filters"  # ID

    ADD_NEW_ADDRESS_BUTTON = 'a[href*="add"]'
    TYPE_CHOICES = "sub_type-"
    CREATE_NEW_CONFIRMATION = "copy_existing"  # ID
    COPY_EXISTING_LINK = "copy"  # ID

    def create_new_or_copy_existing(self, copy_existing: bool):
        if copy_existing:
            self.driver.find_element_by_id(f"{self.CREATE_NEW_CONFIRMATION}-yes").click()
        else:
            self.driver.find_element_by_id(f"{self.CREATE_NEW_CONFIRMATION}-no").click()
        functions.click_submit(self.driver)

    def enter_name(self, name):
        name_tb = self.driver.find_element_by_id(self.INPUT_NAME_ID)
        name_tb.clear()
        name_tb.send_keys(name)

    def get_name(self):
        return self.driver.find_element_by_id(self.INPUT_NAME_ID).get_attribute("value")

    def enter_address(self, address):
        address_tb = self.driver.find_element_by_id(self.INPUT_ADDRESS_ID)
        address_tb.clear()
        address_tb.send_keys(address)

    def get_address(self):
        return self.driver.find_element_by_id(self.INPUT_ADDRESS_ID).get_attribute("value")

    def enter_website(self, website):
        address_tb = self.driver.find_element_by_id(self.INPUT_WEBSITE_ID)
        address_tb.clear()
        address_tb.send_keys(website)

    def get_website(self):
        return self.driver.find_element_by_id(self.INPUT_WEBSITE_ID).get_attribute("value")

    def enter_country(self, country):
        country_tb = self.driver.find_element_by_id(self.INPUT_COUNTRY_ID)
        country_tb.send_keys(country)

    def get_country(self):
        return self.driver.find_element_by_id(self.INPUT_COUNTRY_ID).get_attribute("value")

    def select_type(self, string):
        self.driver.find_element_by_id(self.TYPE_CHOICES + string).click()

    def click_copy_existing_button(self):
        self.driver.find_element_by_id(self.COPY_EXISTING_LINK).click()

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
