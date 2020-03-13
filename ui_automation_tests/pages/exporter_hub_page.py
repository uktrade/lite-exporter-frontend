from ui_automation_tests.shared.BasePage import BasePage


class ExporterHubPage(BasePage):
    APPLY_FOR_A_LICENCE_BTN = "a[href*='/apply-for-a-licence/']"
    APPLICATIONS_BTN = "a[href*='/applications/']"
    MY_GOODS_BTN = "a[href*='/goods/']"
    TILE_MANAGE_MY_ORGANISATION_SELECTOR = "a[href='/organisation/']"
    END_USER_ADVISORY_TILE = "a[href*='/end-users/']"
    RAISE_HMRC_QUERY_BTN = "a[href*='/raise-a-query/"
    USER_PROFILE_BTN = "a[href*='/users/profile/']"

    def click_apply_for_a_licence(self):
        self.driver.find_element_by_css_selector(self.APPLY_FOR_A_LICENCE_BTN).click()

    def click_raise_hmrc_query(self):
        self.driver.find_element_by_css_selector(self.RAISE_HMRC_QUERY_BTN).click()

    def click_applications(self):
        self.driver.find_element_by_css_selector(self.APPLICATIONS_BTN).click()

    def click_end_user_advisories(self):
        self.driver.find_element_by_css_selector(self.END_USER_ADVISORY_TILE).click()

    def click_my_goods(self):
        self.driver.find_element_by_css_selector(self.MY_GOODS_BTN).click()

    def click_manage_my_organisation_tile(self):
        self.driver.find_element_by_css_selector(self.TILE_MANAGE_MY_ORGANISATION_SELECTOR).click()

    def click_user_profile(self):
        self.driver.find_element_by_css_selector(self.USER_PROFILE_BTN).click()
