from ui_automation_tests.shared.BasePage import BasePage


class ExporterHubPage(BasePage):
    APPLY_FOR_A_LICENCE_BTN_ID = "apply-link"
    APPLICATIONS_BTN_ID = "applications-link"
    MY_GOODS_BTN_ID = "products-link"
    MY_PROFILE_BTN_ID = "profile-link"
    EUA_BTN_ID = "eua-link"
    LICENCES_BTN_ID = "licences-link"
    RAISE_HMRC_QUERY_BTN = "a[href*='/raise-a-query/"
    USER_PROFILE_BTN = "a[href*='/users/profile/']"

    def click_apply_for_a_licence(self):
        self.driver.find_element_by_id(self.APPLY_FOR_A_LICENCE_BTN_ID).click()

    def click_raise_hmrc_query(self):
        self.driver.find_element_by_css_selector(self.RAISE_HMRC_QUERY_BTN).click()

    def click_applications(self):
        self.driver.find_element_by_id(self.APPLICATIONS_BTN_ID).click()

    def click_end_user_advisories(self):
        self.driver.find_element_by_id(self.EUA_BTN_ID).click()

    def click_my_goods(self):
        self.driver.find_element_by_id(self.MY_GOODS_BTN_ID).click()

    def click_licences(self):
        self.driver.find_element_by_id(self.LICENCES_BTN_ID).click()

    def click_manage_my_organisation_tile(self):
        self.driver.find_element_by_id(self.MY_PROFILE_BTN_ID).click()

    def click_user_profile(self):
        self.driver.find_element_by_css_selector(self.USER_PROFILE_BTN).click()
