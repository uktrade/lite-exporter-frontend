from pages.exporter_hub_page import ExporterHubPage
from selenium.webdriver.common.by import By
import helpers.helpers as utils
import pytest
import  logging
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
def open_exporter_hub(driver, url):
    # navigate to the application home page
    driver.get(url)
    # driver.maximize_window()
    log.info(driver.current_url)


def test_new_organisation_setup(driver, open_internal_hub):
    log.info("Setting up new organisation")

    manage_organisations_btn = driver.find_element_by_css_selector("a[href*='/organisations']")
    manage_organisations_btn.click()

    exists = utils.is_element_present(driver, By.XPATH ,"//*[text()[contains(.,'Test Org')]]")
    if not exists:
        # New Organisation
        new_organisation_btn = driver.find_element_by_css_selector("a[href*='/register']")
        new_organisation_btn.click()
        business_name_input = driver.find_element_by_id("name")
        eori_number_input = driver.find_element_by_id("eori_number")
        sic_number_input = driver.find_element_by_id("sic_number")
        vat_number_input = driver.find_element_by_id("vat_number")
        company_registration_number = driver.find_element_by_id("registration_number")
        address_input = driver.find_element_by_id("address")
        admin_user_email_input = driver.find_element_by_id("admin_user_email")

        business_name_input.send_keys("Test Org")
        eori_number_input.send_keys("GB987654312000")
        sic_number_input.send_keys("73200")
        vat_number_input.send_keys("123456789")
        company_registration_number.send_keys("000000011")
        address_input.send_keys("123 Cobalt Street")
        admin_user_email_input.send_keys("test@mail.com")

        submit = driver.find_element_by_xpath("//*[@action='submit']")
        submit.click()
        # assert driver.find_element_by_tag_name("h1").text == "Organisations", \
        #     "Failed to return to Organisations list page after submitting new organisation"
        exists = utils.is_element_present(driver, By.XPATH, "//*[text()[contains(.,'Test Org')]]")
        assert exists


def test_add_goods_setup(driver, open_exporter_hub):
    log.info("add 3 goods")
    exporter_hub = ExporterHubPage(driver)
    exporter_hub.login("test@mail.com", "password")

    # Click My goods assert is on the my goods page
    exporter_hub.click_my_goods()

    exists = utils.is_element_present(driver, By.XPATH, "//*[text()[contains(.,'Good T1')]]")
    if not exists:
        # Add good details
        exporter_hub.click_add_a_good()
        exporter_hub.enter_description_of_goods("Good T1")
        exporter_hub.select_is_your_good_controlled("Yes")
        exporter_hub.enter_control_code("ML6")
        exporter_hub.select_is_your_good_intended_to_be_incorporated_into_an_end_product("Yes")
        exporter_hub.enter_part_number("G1-12")
        exporter_hub.click_save_and_continue()

    exists = utils.is_element_present(driver, By.XPATH, "//*[text()[contains(.,'Good T2')]]")
    if not exists:
        exporter_hub.click_add_a_good()
        exporter_hub.enter_description_of_goods("Good T2")
        exporter_hub.select_is_your_good_controlled("Yes")
        exporter_hub.enter_control_code("ML34a")
        exporter_hub.select_is_your_good_intended_to_be_incorporated_into_an_end_product("Yes")
        exporter_hub.enter_part_number("G2-23")
        exporter_hub.click_save_and_continue()

    exists = utils.is_element_present(driver, By.XPATH, "//*[text()[contains(.,'Good T3')]]")
    if not exists:
        exporter_hub.click_add_a_good()
        exporter_hub.enter_description_of_goods("Good T3")
        exporter_hub.select_is_your_good_controlled("Yes")
        exporter_hub.enter_control_code("ML1")
        exporter_hub.select_is_your_good_intended_to_be_incorporated_into_an_end_product("Yes")
        exporter_hub.enter_part_number("G3-3")
        exporter_hub.click_save_and_continue()


def test_teardown(driver):
    driver.quit()

