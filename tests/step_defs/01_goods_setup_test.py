from pytest_bdd import scenarios, given, when, then, parsers
from selenium.webdriver.common.by import By
import helpers.helpers as utils
from pages.exporter_hub_page import ExporterHubPage
from pages.goods_list import GoodsList

scenarios('../features/add_goods.feature')


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

@then(parsers.parse('I see good "{good}" in goods list part number "{partno}" control code "{controlcode}"'))
def assert_good_is_in_list(driver, good, partno, controlcode):
    goods_list = GoodsList(driver)
    goods_list.assert_goods_are_displayed_of_good_name(good, partno, controlcode)
