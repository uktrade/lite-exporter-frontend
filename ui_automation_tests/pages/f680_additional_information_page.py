from ui_automation_tests.shared import functions
from ui_automation_tests.shared.BasePage import BasePage


class F680AdditionalInformationPage(BasePage):
    DATE_DAY_ID = "day"
    DATE_MONTH_ID = "month"
    DATE_YEAR_ID = "year"

    def enter_date_of_issue(self, day, month, year):
        self.driver.find_element_by_id(self.DATE_DAY_ID).send_keys(day)
        self.driver.find_element_by_id(self.DATE_MONTH_ID).send_keys(month)
        self.driver.find_element_by_id(self.DATE_YEAR_ID).send_keys(year)
        functions.click_submit(self.driver)
