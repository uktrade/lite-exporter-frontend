class Hub():

    def __init__(self, driver):
        self.driver = driver
        self.drafts_btn = "a[href*='/drafts/']"
        self.application_btn = "a[href*='/applications/']"

    def click_drafts(self):
        self.driver.find_element_by_css_selector(self.drafts_btn).click()

    def click_applications(self):
        self.driver.find_element_by_css_selector(self.application_btn).click()
