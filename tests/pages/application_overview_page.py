class ApplicationOverviewPage():

    def __init__(self, driver):
        self.driver = driver
        self.sites_link = "location" #id
        self.goods_link = "goods"

    def click_application_locations_link(self):
        self.driver.find_element_by_css_selector(self.sites_link).click()

    def click_goods_link(self):
        self.driver.find_element_by_id(self.goods_link).click()
