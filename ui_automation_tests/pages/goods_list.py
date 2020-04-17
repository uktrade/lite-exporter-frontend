from pages.shared import Shared
from shared import functions
from ui_automation_tests.shared.BasePage import BasePage


class GoodsListPage(BasePage):

    BUTTON_ADD_A_GOOD_ID = "button-add-a-good"
    INPUT_DESCRIPTION_FILTER_ID = "description"

    def click_view_good(self, index: int):
        """
        Clicks the view link on a table row at the index given.
        Args:
            index: Index of good in table, starts at 0
        """
        self.driver.find_elements_by_css_selector(f"{Shared.GOV_TABLE_ROW}:nth-of-type({index + 1}) a")[-1].click()

    def click_add_a_good(self):
        self.driver.find_element_by_id(self.BUTTON_ADD_A_GOOD_ID).click()

    def filter_by_description(self, description: str):
        functions.try_open_filters(self.driver)
        self.driver.find_element_by_id(self.INPUT_DESCRIPTION_FILTER_ID).clear()
        self.driver.find_element_by_id(self.INPUT_DESCRIPTION_FILTER_ID).send_keys(description)
        self.driver.find_element_by_id("button-apply-filters").click()
