from pytest_bdd import when, scenarios, then, given, parsers

from pages.application_overview_page import OpenApplicationOverviewPage
from pages.application_page import ApplicationPage
from ui_automation_tests.pages.application_goods_type_list import ApplicationGoodsTypeList

scenarios("../features/edit_open_application.feature", strict_gherkin=False)


@given("I create an open application via api")
def open_application_exists(apply_for_open_application):
    pass


@when("I remove a good type from the application")
def i_remove_a_good_from_the_application(driver):
    remove_good_link = OpenApplicationOverviewPage(driver).find_remove_goods_type_link()
    driver.execute_script("arguments[0].click();", remove_good_link)


@then("no goods types are left on the application")
def no_goods_types_are_left_on_the_application(driver):
    assert (ApplicationGoodsTypeList(driver).find_remove_goods_type_link(), None)


@when("I click on open goods tile")  # noqa
def click_my_goods_link(driver):  # noqa
    exporter_hub = OpenApplicationOverviewPage(driver)
    exporter_hub.click_open_goods_link()
