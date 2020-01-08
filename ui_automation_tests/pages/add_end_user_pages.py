from shared.BasePage import BasePage
from shared import functions


class AddEndUserPages(BasePage):
    ADD_NEW_ADDRESS_BUTTON = 'a[href*="add"]'
    TYPE_CHOICES = "sub_type-"
    CREATE_NEW_CONFIRMATION = "copy_existing"  # ID

    def create_new_or_copy_existing(self, copy_existing: bool):
        if copy_existing:
            self.driver.find_element_by_id(f"{self.CREATE_NEW_CONFIRMATION}-yes").click()
        else:
            self.driver.find_element_by_id(f"{self.CREATE_NEW_CONFIRMATION}-no").click()
        functions.click_submit(self.driver)

    def enter_name(self, name):
        name_tb = self.driver.find_element_by_id("name")
        name_tb.clear()
        name_tb.send_keys(name)

    def enter_address(self, address):
        address_tb = self.driver.find_element_by_id("address")
        address_tb.clear()
        address_tb.send_keys(address)

    def enter_website(self, website):
        address_tb = self.driver.find_element_by_id("website")
        address_tb.clear()
        address_tb.send_keys(website)

    def enter_country(self, country):
        country_tb = self.driver.find_element_by_id("country")
        country_tb.send_keys(country)

    def select_type(self, string):
        self.driver.find_element_by_id(self.TYPE_CHOICES + string).click()
