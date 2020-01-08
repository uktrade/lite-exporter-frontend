from shared.BasePage import BasePage
from shared.tools.helpers import scroll_to_element_by_id


class OpenApplicationAddGoodsType(BasePage):

    INPUT_DESCRIPTION_ID = "description"
    INPUT_CONTROL_CODE_ID = "control_code"
    RADIO_IS_GOOD_CONTROLLED_ID = "is_good_controlled-"
    RADIO_IS_GOOD_INCORPORATED_ID = "is_good_end_product-"

    def enter_description(self, value):
        self.driver.find_element_by_id(self.INPUT_DESCRIPTION_ID).send_keys(value)

    def select_is_your_good_controlled(self, value):
        self.driver.find_element_by_id(self.RADIO_IS_GOOD_CONTROLLED_ID + value.lower()).click()

    def enter_control_code(self, value):
        self.driver.find_element_by_id(self.INPUT_CONTROL_CODE_ID).send_keys(value)
        # This is done as control code textbox needs to lose focus
        self.driver.find_element_by_tag_name("body").click()

    def select_is_your_good_incorporated(self, value):
        self.driver.find_element_by_id(self.RADIO_IS_GOOD_INCORPORATED_ID + value.lower()).click()
