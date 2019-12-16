from shared.BasePage import BasePage


class MemberPage(BasePage):

    PANE_MORE_ACTIONS_HIDDEN_SELECTOR = "lite-more-actions__container--hidden"
    BUTTON_REACTIVATE_ID = "button-reactivate"
    BUTTON_DEACTIVATE_ID = "button-deactivate"
    BUTTON_REACTIVATE_CONFIRM_ID = "reactivate-confirm"
    BUTTON_DEACTIVATE_CONFIRM_ID = "deactivate-confirm"
    BUTTON_MORE_ACTIONS_ID = "button-more-actions"
    BUTTON_ADD_A_MEMBER_ID = "button-add-a-member"

    def click_add_a_member_button(self):
        self.driver.find_element_by_id(self.BUTTON_ADD_A_MEMBER_ID).click()

    def try_click_more_actions_button(self):
        if self.driver.find_elements_by_class_name(self.PANE_MORE_ACTIONS_HIDDEN_SELECTOR):
            self.driver.find_element_by_id(self.BUTTON_MORE_ACTIONS_ID).click()

    def click_deactivate_button(self):
        self.try_click_more_actions_button()
        self.driver.find_element_by_id(self.BUTTON_DEACTIVATE_ID).click()
        self.driver.find_element_by_id(self.BUTTON_DEACTIVATE_CONFIRM_ID).click()

    def click_reactivate_button(self):
        self.try_click_more_actions_button()
        self.driver.find_element_by_id(self.BUTTON_REACTIVATE_ID).click()
        self.driver.find_element_by_id(self.BUTTON_REACTIVATE_CONFIRM_ID).click()
