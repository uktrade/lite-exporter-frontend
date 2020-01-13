from shared.BasePage import BasePage
from shared import functions


class AddEndUserPages(BasePage):
    INPUT_NAME_ID = "name"  # ID
    INPUT_ADDRESS_ID = "address"  # ID
    INPUT_COUNTRY_ID = "country"  # ID
    INPUT_WEBSITE_ID = "website"  # ID

    LINK_SHOW_FILTER_ID = "show-filters-link"
    INPUT_FILTER_NAME_ID = "name"
    INPUT_FILTER_ADDRESS_ID = "address"
    INPUT_FILTER_COUNTRY_ID = "country"
    BUTTON_SUBMIT_FILTER_ID = "button-apply-filters"

    INPUT_PARTY_TYPE_ID = "sub_type-"
    INPUT_CREATE_NEW_OR_COPY_ID = "copy_existing"  # ID
    LINK_COPY_EXISTING_ID = "copy"  # ID

    def create_new_or_copy_existing(self, copy_existing: bool):
        if copy_existing:
            self.driver.find_element_by_id(f"{self.INPUT_CREATE_NEW_OR_COPY_ID}-yes").click()
        else:
            self.driver.find_element_by_id(f"{self.INPUT_CREATE_NEW_OR_COPY_ID}-no").click()
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
        self.driver.find_element_by_id(self.INPUT_PARTY_TYPE_ID + string).click()

    def click_copy_existing_button(self):
        self.driver.find_element_by_id(self.LINK_COPY_EXISTING_ID).click()

    def open_parties_filter(self):
        self.driver.find_element_by_id(self.LINK_SHOW_FILTER_ID).click()

    def filter_name(self, text):
        self.driver.find_element_by_id(self.INPUT_FILTER_NAME_ID).send_keys(text)

    def filter_address(self, text):
        self.driver.find_element_by_id(self.INPUT_FILTER_ADDRESS_ID).send_keys(text)

    def filter_country(self, text):
        self.driver.find_element_by_id(self.INPUT_FILTER_COUNTRY_ID).send_keys(text)

    def submit_filter(self):
        self.driver.find_element_by_id(self.BUTTON_SUBMIT_FILTER_ID).click()
