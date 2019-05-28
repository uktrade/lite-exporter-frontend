from pytest_bdd import scenarios, given, when, then, parsers
from selenium.webdriver.common.by import By
from pages.internal_hub_page import InternalHubPage
import helpers.helpers as utils
from pages.exporter_hub_page import ExporterHubPage
scenarios('../features/add_goods_setup.feature')

@when('I click on goods link')
def click_my_goods_link(driver):
    exporter_hub = ExporterHubPage(driver)
    exporter_hub.click_my_goods()

@when(parsers.parse('I add a good with description "{description}" controlled "{controlled}" control code "{controlcode}" incorporated "{incorporated}" and part number "{part}"'))
def add_new_good(driver, description, controlled,  controlcode, incorporated, part):
    exporter_hub = ExporterHubPage(driver)
    exists = utils.is_element_present(driver, By.XPATH, "//*[text()[contains(.,'"+description+"')]]")
    if not exists:
        exporter_hub.click_add_a_good()
        exporter_hub.enter_description_of_goods(description)
        exporter_hub.select_is_your_good_controlled(controlled)
        exporter_hub.enter_control_code(controlcode)
        exporter_hub.select_is_your_good_intended_to_be_incorporated_into_an_end_product(incorporated)
        exporter_hub.enter_part_number(part)
        exporter_hub.click_save_and_continue()

