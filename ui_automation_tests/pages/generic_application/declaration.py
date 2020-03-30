from ui_automation_tests.shared.BasePage import BasePage
from ui_automation_tests.shared.tools.helpers import scroll_to_element_by_id


class DeclarationPage(BasePage):
    FOI_ID = "agreed_to_foi-True"
    DECLARATION_ID = "I have read and agreed to the terms and conditions of the licence I am applying for"

    def agree_to_foi(self):
        scroll_to_element_by_id(self.driver, self.FOI_ID)
        self.driver.find_element_by_id(self.FOI_ID).click()

    def agree_to_declaration(self):
        scroll_to_element_by_id(self.driver, self.DECLARATION_ID)
        self.driver.find_element_by_id(self.DECLARATION_ID).click()
