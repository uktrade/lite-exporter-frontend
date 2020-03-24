from ui_automation_tests.shared import functions
from ui_automation_tests.shared.BasePage import BasePage


class F680AdditionalInformationPage(BasePage):
    DATE_DAY_ID = "day"
    DATE_MONTH_ID = "month"
    DATE_YEAR_ID = "year"
    EXPEDITED_ID = "expedited-{value}"
    FOREIGN_TECHNOLOGY_ID = "foreign_technology-{value}"
    LOCALLY_MANUFACTURED_ID = "locally_manufactured-{value}"
    ELECTRONIC_WARFARE_REQUIREMENT_ID = "electronic_warfare_requirement-{value}"
    MTCR_TYPE_ID = "mtcr_type-{value}"
    UK_SERVICE_EQUIPMENT_ID = "uk_service_equipment-{value}"
    UK_SERVICE_EQUIPMENT_TYPE_ID = "uk_service_equipment_type-{value}"
    PROSPECT_VALUE_ID = "prospect_value"

    def enter_date_of_issue(self, day, month, year):
        self.driver.find_element_by_id(self.DATE_DAY_ID).send_keys(day)
        self.driver.find_element_by_id(self.DATE_MONTH_ID).send_keys(month)
        self.driver.find_element_by_id(self.DATE_YEAR_ID).send_keys(year)
        functions.click_submit(self.driver)

    def enter_no_date(self, value=False):
        self.driver.find_element_by_id(self.EXPEDITED_ID.format(value=value)).click()
        functions.click_submit(self.driver)

    def enter_foreign_technology(self, value=False):
        self.driver.find_element_by_id(self.FOREIGN_TECHNOLOGY_ID.format(value=value)).click()
        functions.click_submit(self.driver)

    def enter_locally_manufactured(self, value=False):
        self.driver.find_element_by_id(self.LOCALLY_MANUFACTURED_ID.format(value=value)).click()
        functions.click_submit(self.driver)

    def enter_mtcr_type(self, value="mtcr_category_2"):
        self.driver.find_element_by_id(self.MTCR_TYPE_ID.format(value=value)).click()
        functions.click_submit(self.driver)

    def enter_electronic_warfare_requirement(self, value=False):
        self.driver.find_element_by_id(self.ELECTRONIC_WARFARE_REQUIREMENT_ID.format(value=value)).click()
        functions.click_submit(self.driver)

    def enter_uk_service_equipment(self, value=False):
        self.driver.find_element_by_id(self.UK_SERVICE_EQUIPMENT_ID.format(value=value)).click()
        functions.click_submit(self.driver)

    def enter_uk_service_equipment_type(self, value="mod_funded"):
        self.driver.find_element_by_id(self.UK_SERVICE_EQUIPMENT_TYPE_ID.format(value=value)).click()
        functions.click_submit(self.driver)

    def enter_prospect_value(self, value="100.00"):
        functions.enter_value(self.driver, element_id=self.PROSPECT_VALUE_ID, value=value)
        functions.click_submit(self.driver)
