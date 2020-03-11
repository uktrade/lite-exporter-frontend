from ui_automation_tests.shared.BasePage import BasePage


class EndUseDetailsFormPage(BasePage):
    def click_on_yes_radiobutton(self):
        self.driver.find_element_by_xpath("//input[@value='True']").click()

    def click_on_no_radiobutton(self):
        self.driver.find_element_by_xpath("//input[@value='False']").click()

    def enter_reference_number(self):
        ref_field = self.driver.find_element_by_class_name("govuk-input")
        ref_field.clear()
        ref_field.send_keys("JKHBA489129")

    def enter_additional_details(self):
        details_field = self.driver.find_element_by_class_name("govuk-textarea").click()
        details_field.clear()
        details_field.send_keys("jhkfsahjkfakbjnfkbjefbjkefskbjfeasbkjfaeskbjfeakbjbjknaefsbkjasefkbjfewbk")
