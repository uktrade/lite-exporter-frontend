from ui_automation_tests.pages.BasePage import BasePage


class GoodsPage(BasePage):

    LINK_EDIT_ID = "link-edit"
    QUERY_TABLE_ID = "query_table"
    BUTTON_DELETE_GOOD_ID = "button-delete-good"

    LINK_EDIT_GOOD_MILITARY_USE_ID = "change-good-military-use"
    LINK_EDIT_GOOD_IS_COMPONENT_ID = "change-good-is-component"
    LINK_EDIT_GOOD_USES_INFOSEC_ID = "change-good-information-security"
    LINK_EDIT_GOOD_SOFTWARE_TECHNOLOGY_ID = "change-good-technology-software"

    LINK_EDIT_FIREARM_GOOD_PRODUCT_TYPE_ID = "change-product-type"
    LINK_EDIT_FIREARM_GOOD_FIREARMS_ACT_ID = "change-firearms-act-details"
    LINK_EDIT_FIREARM_GOOD_IDENTIFICATION_MARKINGS_ID = "change-identification-markings"

    def click_on_goods_description_edit_link(self):
        self.driver.find_element_by_id(self.LINK_EDIT_ID).click()

    def click_on_good_edit_military_use_link(self):
        self.driver.find_element_by_id(self.LINK_EDIT_GOOD_MILITARY_USE_ID).click()

    def click_on_good_edit_is_component_link(self):
        self.driver.find_element_by_id(self.LINK_EDIT_GOOD_IS_COMPONENT_ID).click()

    def click_on_good_edit_uses_information_security_link(self):
        self.driver.find_element_by_id(self.LINK_EDIT_GOOD_USES_INFOSEC_ID).click()

    def click_on_good_edit_software_technology_details(self):
        self.driver.find_element_by_id(self.LINK_EDIT_GOOD_SOFTWARE_TECHNOLOGY_ID).click()

    def click_on_firearm_good_edit_product_type_link(self):
        self.driver.find_element_by_id(self.LINK_EDIT_FIREARM_GOOD_PRODUCT_TYPE_ID)

    def click_on_firearm_good_edit_firearms_act_sections_applicable_link(self):
        self.driver.find_element_by_id(self.LINK_EDIT_FIREARM_GOOD_FIREARMS_ACT_ID)

    def click_on_firearm_good_edit_identification_markings_link(self):
        self.driver.find_element_by_id(self.LINK_EDIT_FIREARM_GOOD_IDENTIFICATION_MARKINGS_ID)

    def get_text_of_query_details(self):
        return self.driver.find_element_by_id(self.QUERY_TABLE_ID)

    def click_delete_button(self):
        self.driver.find_element_by_id(self.BUTTON_DELETE_GOOD_ID).click()
