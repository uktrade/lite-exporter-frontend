from ui_automation_tests.shared.BasePage import BasePage


class EndUseDetailsFormPage(BasePage):
    def click_on_yes_radiobutton(self):
        self.driver.find_element_by_css_selector('[id$=-True]').click()

    def click_on_no_radiobutton(self):
        self.driver.find_element_by_css_selector('[id$=-False]').click()

    def enter_reference_number(self):
        ref_field = self.driver.find_element_by_class_name("govuk-input")
        ref_field.clear()
        ref_field.send_keys("JKHBA489129")

    def enter_additional_details(self):
        id = "compliant_limitations_eu_ref"
        # suspected_wmd_ref
        self.driver.execute_script(f'document.getElementById("{id}").value = "ababcc"')
        self.driver.find_element_by_id(id).send_keys("ababcc")


