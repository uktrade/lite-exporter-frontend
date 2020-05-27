from selenium.webdriver.remote.webdriver import WebDriver

from ui_automation_tests.shared import functions


class BasePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
