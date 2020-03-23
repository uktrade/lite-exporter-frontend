from random import randint

from conftest import fake
from shared import functions
from shared.BasePage import BasePage


class RegisterOrganisation(BasePage):
    CREATE_ACCOUNT_ID = "button-Create an account"
    COMMERCIAL_INDIVIDUAL_PARTIAL_ID = "type-"
    INDIVIDUAL_RADIO_ID = "type-individual"
    COMPANY_NAME_ID = "name"
    EORI_ID = "eori_number"
    SIC_ID = "sic_number"
    VAT_ID = "vat_number"
    REG_ID = "registration_number"
    SITE_NAME_ID = "site.name"
    SITE_ADDRESS_LINE_1_ID = "site.address.address_line_1"
    SITE_CITY_ID = "site.address.city"
    SITE_REGION_ID = "site.address.region"
    SITE_POSTCODE_ID = "site.address.postcode"
    SITE_COUNTRY_ID = "site.address.country"

    def click_create_an_account_button(self):
        self.driver.find_element_by_id(self.CREATE_ACCOUNT_ID).click()

    def select_commercial_or_individual_organisation(self, selection):
        self.driver.find_element_by_id(self.COMMERCIAL_INDIVIDUAL_PARTIAL_ID + selection).click()

    def enter_random_company_name(self):
        self.driver.find_element_by_id(self.COMPANY_NAME_ID).send_keys(fake.company())

    def enter_random_eori_number(self):
        self.driver.find_element_by_id(self.EORI_ID).send_keys(randint(10000, 99999))

    def enter_random_sic_number(self):
        self.driver.find_element_by_id(self.SIC_ID).send_keys(randint(10000, 99999))

    def enter_random_vat_number(self):
        self.driver.find_element_by_id(self.VAT_ID).send_keys("GB" + str(randint(1000000, 9999999)))

    def enter_random_registration_number(self):
        self.driver.find_element_by_id(self.REG_ID).send_keys(randint(10000000, 99999999))

    def enter_random_site(self):
        self.driver.find_element_by_id(self.SITE_NAME_ID).send_keys(fake.secondary_address())
        self.driver.find_element_by_id(self.SITE_ADDRESS_LINE_1_ID).send_keys(fake.street_address())
        self.driver.find_element_by_id(self.SITE_CITY_ID).send_keys(fake.city())
        self.driver.find_element_by_id(self.SITE_REGION_ID).send_keys(fake.state())
        self.driver.find_element_by_id(self.SITE_POSTCODE_ID).send_keys(fake.postcode())
        functions.send_keys_to_autocomplete(self.driver, self.SITE_COUNTRY_ID, "Canada")
