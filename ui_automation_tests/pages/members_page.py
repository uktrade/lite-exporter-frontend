from shared.BasePage import BasePage


class MembersPage(BasePage):

    BUTTON_ADD_A_MEMBER_ID = "button-add-a-member"

    def click_add_a_member_button(self):
        self.driver.find_element_by_id(self.BUTTON_ADD_A_MEMBER_ID).click()
