from shared import selectors
from shared.BasePage import BasePage


class StandardApplicationGoodsPage(BasePage):

    BUTTON_ADD_NEW_GOOD_ID = "button-add-new-good"
    BUTTON_ADD_PREEXISTING_GOOD_ID = "button-add-preexisting-good"
    SPAN_GOODS_TOTAL_VALUE = "span-goods-total-value"
    BUTTON_ADD_NEW_GOOD = "add-new"  # ID
    quantity_field = "quantity"  # ID
    unit_dropdown = "unit"  # ID
    value_field = "value"  # ID
    filter_description_search_box = "description"  # ID
    filter_part_number_search_box = "part_number"  # ID
    filter_control_rating_search_box = "control_rating"  # ID
    filter_button = "button-apply-filters"  # ID
    card_label = ".lite-card .govuk-label"
    part_number = "good-part-number"
    show_filters_link = "show-filters-link"  # ID
    description = "good-description"
    control_code = "good-control_code"
    good_entry = ".govuk-table__body .govuk-table__row"

    def click_add_new_good_button(self):
        self.driver.find_element_by_id(self.BUTTON_ADD_NEW_GOOD_ID).click()

    def click_add_preexisting_good_button(self):
        self.driver.find_element_by_id(self.BUTTON_ADD_PREEXISTING_GOOD_ID).click()

    def get_goods(self):
        return self.driver.find_elements_by_css_selector(selectors.TABLE_BODY + " " + selectors.TABLE_ROW)

    def get_goods_total_value(self):
        return self.driver.find_element_by_id(self.SPAN_GOODS_TOTAL_VALUE).text

    # old
    def type_into_filter_description_search_box_and_filter(self, value):
        self.driver.find_element_by_id(self.show_filters_link).click()
        self.driver.find_element_by_id(self.filter_description_search_box).send_keys(value)
        self.driver.find_element_by_id(self.filter_button).click()

    def type_into_filter_part_number_search_box_and_filter(self, value):
        self.driver.find_element_by_id(self.filter_part_number_search_box).send_keys(value)
        self.driver.find_element_by_id(self.filter_button).click()

    def type_into_filter_control_rating_search_box_and_filter(self, value):
        self.driver.find_element_by_id(self.filter_control_rating_search_box).send_keys(value)
        self.driver.find_element_by_id(self.filter_button).click()

    def get_good_descriptions(self):
        return self.driver.find_elements_by_id(self.description)

    def get_good_part_numbers(self):
        return self.driver.find_elements_by_id(self.part_number)

    def get_good_control_codes(self):
        return self.driver.find_elements_by_id(self.control_code)

    def click_add_new_good_button(self):
        return self.driver.find_element_by_id(self.BUTTON_ADD_NEW_GOOD).click()

    def get_goods_count(self):
        return len(self.driver.find_elements_by_css_selector(self.good_entry))