import random
from pytest_bdd import scenarios, given, when, then, parsers
from pages.goods_list import GoodsList
from pages.exporter_hub_page import ExporterHubPage
from pages.add_goods_page import AddGoodPage
from conftest import context

scenarios('../features/add_goods.feature', strict_gherkin=False)


@when('I click on goods link')
def click_my_goods_link(driver):
    exporter_hub = ExporterHubPage(driver)
    exporter_hub.click_my_goods()


@when(parsers.parse('I add a good with description "{description}" controlled "{controlled}" control code "{controlcode}" incorporated "{incorporated}" and part number "{part}"'))
def add_new_good(driver, description, controlled,  controlcode, incorporated, part):
    exporter_hub = ExporterHubPage(driver)
    add_goods_page = AddGoodPage(driver)
    good_description = description + str(random.randint(1, 100))
    context.good_description = good_description
    context.part = part
    context.controlcode = controlcode
    add_goods_page.click_add_a_good()
    add_goods_page.enter_description_of_goods(good_description)
    add_goods_page.select_is_your_good_controlled(controlled)
    add_goods_page.enter_control_code(controlcode)
    add_goods_page.select_is_your_good_intended_to_be_incorporated_into_an_end_product(incorporated)
    add_goods_page.enter_part_number(part)
    exporter_hub.click_save_and_continue()


@then('I see good in goods list')
def assert_good_is_in_list(driver):
    goods_list = GoodsList(driver)
    goods_list.assert_goods_are_displayed_of_good_name(context.good_description, context.part, context.controlcode)
