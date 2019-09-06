

class EndUserAdvisoryPage:

    def __init__(self, driver):
        self.driver = driver

        self.apply_for_advisory = "a[href*='/end-users/apply-for-an-advisory']"

    def click_apply_for_advisories(self):
        self.driver.find_element_by_css_selector(self.apply_for_advisory).click()
