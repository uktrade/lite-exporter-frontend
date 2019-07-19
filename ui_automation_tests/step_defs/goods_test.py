from pytest_bdd import scenarios, given, when, then, parsers
from pages.goods_list import GoodsList
from pages.exporter_hub_page import ExporterHubPage
from pages.add_goods_page import AddGoodPage
from conftest import context

scenarios('../features/add_goods.feature', strict_gherkin=False)


@then('I see good in goods list')
def assert_good_is_in_list(driver):
    goods_list = GoodsList(driver)
    goods_list.assert_goods_are_displayed_of_good_name(context.good_description, context.part, context.control_code)


@when(parsers.parse('I edit a good to description "{description}" controlled "{controlled}" control code "{control_code}" incorporated "{incorporated}" and part number "{part}"'))
def edit_good(driver, description, controlled,  control_code, incorporated, part):
    exporter_hub = ExporterHubPage(driver)
    add_goods_page = AddGoodPage(driver)
    goods_list = GoodsList(driver)
    goods_list.click_on_goods_edit_link(0)
    context.edited_description = context.good_description + " " + description
    add_goods_page.enter_description_of_goods(context.edited_description)
    exporter_hub.click_save_and_continue()


@then('I see my edited good in the goods list')
def see_my_edited_good_in_list(driver):
    assert context.edited_description in driver.find_element_by_tag_name("body").text


@when('I delete my good')
def delete_my_good_in_list(driver):
    goods_list = GoodsList(driver)
    driver.find_element_by_css_selector("[href*='goods/delete/']").click()
    goods_list.click_on_delete_good_button()


@then('my good is no longer in the goods list')
def good_is_no_longer_in_list(driver):
    assert len(driver.find_elements_by_css_selector(f'a[text="{context.edited_description}"]')) is 0
