from pages.exporter_hub_page import ExporterHubPage
from selenium.webdriver.common.by import By
import helpers.helpers as utils
import pytest
import logging
from pages.exporter_hub_page import ExporterHubPage
from pages.internal_hub_page import InternalHubPage

log = logging.getLogger()
console = logging.StreamHandler()
log.addHandler(console)

@pytest.fixture(scope="function")
def open_internal_hub(driver, internal_url):
    # navigate to the application home page
    driver.get(internal_url)
    # driver.maximize_window()
    log.info(driver.current_url)

@pytest.fixture(scope="function")
def open_exporter_hub(driver, exporter_url):
    # navigate to the application home page
    driver.get(exporter_url)
    # driver.maximize_window()
    log.info(driver.current_url)


def test_add_users_setup(driver, exporter_url):
    log.info("add test user")
    exporter_hub = ExporterHubPage(driver)
    exporter_hub.go_to(exporter_url)
    if "login" in driver.current_url:
        log.info("logging in as test@mail.com")
        exporter_hub.login("test@mail.com", "password")

    exporter_hub.click_users()
    exists = utils.is_element_present(driver, By.XPATH, "//td[text()[contains(.,'testuser_1@mail.com')]]")
    if not exists:
        for x in range(3):
            i = str(x + 1)
            exporter_hub.click_add_a_user_btn()
            exporter_hub.enter_first_name("Test")
            exporter_hub.enter_last_name("user_" + i)
            exporter_hub.enter_email("testuser_" + i + "@mail.com")
            exporter_hub.enter_password("1234")
            exporter_hub.click_save_and_continue()


def test_teardown(driver):
    driver.quit()
