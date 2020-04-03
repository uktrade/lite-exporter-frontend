from ui_automation_tests.shared.BasePage import BasePage


class LicencesPage(BasePage):
    LICENCE_ROW_PARTIAL_ID = "licence-"
    EXPAND_LICENCE_ROW_PARTIAL_ID = "expand-"

    def licence_row_properties(self, id):
        self.driver.find_element_by_id(self.EXPAND_LICENCE_ROW_PARTIAL_ID + id).click()
        return self.driver.find_element_by_id(self.LICENCE_ROW_PARTIAL_ID + id).text
