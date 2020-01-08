from shared import selectors
from shared.BasePage import BasePage


class StandardApplicationGoodsPage(BasePage):

    BUTTON_ADD_NEW_GOOD_ID = "button-add-new-good"
    BUTTON_ADD_PREEXISTING_GOOD_ID = "button-add-preexisting-good"
    SPAN_GOODS_TOTAL_VALUE = "span-goods-total-value"

    def click_add_new_good_button(self):
        self.driver.find_element_by_id(self.BUTTON_ADD_NEW_GOOD_ID).click()

    def click_add_preexisting_good_button(self):
        self.driver.find_element_by_id(self.BUTTON_ADD_PREEXISTING_GOOD_ID).click()

    def get_goods(self):
        return self.driver.find_elements_by_css_selector(selectors.TABLE_BODY + " " + selectors.TABLE_ROW)

    def get_goods_total_value(self):
        return self.driver.find_element_by_id(self.SPAN_GOODS_TOTAL_VALUE).text
