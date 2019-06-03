class ApplicationOverviewPage():

    def __init__(self, driver):
        self.driver = driver
        self.sites_link = "a[href*='sites']"

    def click_sites_link(self):
        self.driver.find_element_by_css_selector(self.sites_link).click()
