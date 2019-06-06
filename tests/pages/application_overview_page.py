from selenium import webdriver


class ApplicationOverviewPage():

    def __init__(self, driver):
        self.driver = driver
        self.sites_link = "location" #id
        self.goods_link = "goods" #id
        self.end_user_link = "end_users"

    def click_application_locations_link(self):
        element = self.driver.find_element_by_id(self.sites_link)
        self.driver.execute_script("arguments[0].click();", element)

    def click_goods_link(self):
        element = self.driver.find_element_by_id(self.goods_link)
        self.driver.execute_script("arguments[0].click();", element)

    def click_end_user_link(self):
        element = self.driver.find_element_by_id(self.end_user_link)
        self.driver.execute_script("arguments[0].click();", element)
