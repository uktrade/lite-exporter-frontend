from shared.BasePage import BasePage


class ApplicationPage(BasePage):
    BUTTON_WITHDRAW_APPLICATION_ID = "button-withdraw-application"
    BUTTON_EDIT_APPLICATION_ID = "button-edit-application"
    LABEL_APPLICATION_STATUS_ID = "label-application-status"
    ecju_query_tab = "ecju-queries-tab"  # ID
    ecju_query_response_text = 'Respond to query'  # text
    ecju_queries_closed = "closed-ecju-query"  # ID
    edit_application_link = "a[href*='/edit-type/']"

    def click_withdraw_application_button(self):
        self.driver.find_element_by_id(self.BUTTON_WITHDRAW_APPLICATION_ID).click()

    def click_edit_application_link(self):
        self.driver.find_element_by_css_selector(self.edit_application_link).click()

    def click_ecju_query_tab(self):
        self.driver.find_element_by_id(self.ecju_query_tab).click()

    def get_count_of_closed_ecju_queries(self):
        return len(self.driver.find_elements_by_id(self.ecju_queries_closed))

    def respond_to_ecju_query(self, no):
        response = '//a[contains(text(), "' + self.ecju_query_response_text + '")]'
        self.driver.find_elements_by_xpath(response)[no].click()

    def find_edit_application_button(self):
        return self.driver.find_elements_by_id(self.BUTTON_EDIT_APPLICATION_ID)

    def get_status(self):
        return self.driver.find_element_by_id(self.LABEL_APPLICATION_STATUS_ID).text
