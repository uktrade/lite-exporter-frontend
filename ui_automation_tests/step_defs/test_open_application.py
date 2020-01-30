from pytest_bdd import scenarios, when, then, parsers, given

import shared.tools.helpers as utils
from shared import functions
from conftest import (
    click_apply_licence,
    enter_type_of_application,
    enter_application_name,
    enter_permanent_or_temporary,
)
from pages.apply_for_a_licence_page import ApplyForALicencePage
from pages.generic_application.task_list import GenericApplicationTaskListPage
from pages.open_application.countries import OpenApplicationCountriesPage
from pages.open_application.goods_countries_page import GoodsCountriesPage
from pages.open_application.goods_types import OpenApplicationGoodsTypesPage
from pages.open_application.task_list import OpenApplicationTaskListPage
from pages.shared import Shared

scenarios(
    "../features/submit_open_application.feature", "../features/edit_open_application.feature", strict_gherkin=False
)


@then("I see good types error messages")
def goods_type_errors(driver):
    shared = Shared(driver)
    assert "This field may not be blank." in shared.get_text_of_error_messages()
    assert "This field is required." in shared.get_text_of_error_messages()


@then(parsers.parse('I see my goods type added at position "{position}" with a description and a control code'))
def i_see_the_goods_types_list(driver, position, context):
    goods_type_page = OpenApplicationGoodsTypesPage(driver)
    good_type = goods_type_page.get_text_of_goods_type_info(int(position))
    assert context.good_description in good_type
    assert context.control_code in good_type


@when("I click on countries")
def i_click_on_countries(driver):
    OpenApplicationTaskListPage(driver).click_countries_link()


@then("I should see a list of countries")
def i_should_see_a_list_of_countries(driver):
    application_countries_list = OpenApplicationCountriesPage(driver)
    page_countries = application_countries_list.get_countries_names()
    assert len(page_countries) == 274


@when(parsers.parse('I select "{country}" from the country list'))
def i_select_country_from_the_country_list(driver, country):
    application_countries_list = OpenApplicationCountriesPage(driver)
    application_countries_list.select_country(country)

    assert utils.find_element_by_href(driver, "#" + country).is_displayed()


@when(parsers.parse('I search for country "{country}"'))
def search_for_country(driver, country):
    OpenApplicationCountriesPage(driver).search_for_country(country)


@then(parsers.parse('only "{country}" is displayed in country list'))
def search_country_result(driver, country):
    assert (
        country == OpenApplicationCountriesPage(driver).get_text_of_countries_list()
    ), "Country not searched correctly"


@when("I click on assign countries to goods")
def go_to_good_countries(driver):
    page = GenericApplicationTaskListPage(driver)
    page.click_goods_countries_link()


@when("I click select all countries")
def select_all_countries(driver):
    page = OpenApplicationCountriesPage(driver)
    page.click_select_all()


@then("all checkboxes are selected")
def all_selected(driver):
    page = OpenApplicationCountriesPage(driver)
    assert page.get_number_of_checkboxes(checked=False) == page.get_number_of_checkboxes(checked=True)


@when(parsers.parse('I "{assign_or_unassign}" all countries to all goods with link'))
def assign_all_with_link(driver, assign_or_unassign):
    countries_page = GoodsCountriesPage(driver)
    if assign_or_unassign == "assign":
        countries_page.select_all_link()
        countries_page.click_save()
    else:
        countries_page.deselect_all_link()


@when("I click Add goods type button")
def click_goods_type_button(driver):
    goods_type_page = OpenApplicationGoodsTypesPage(driver)
    goods_type_page.click_goods_type_button()


@then(parsers.parse('I see all countries are "{assigned_or_unassigned}" to all goods'))
def see_all_or_no_selected(driver, assigned_or_unassigned):
    countries_page = GoodsCountriesPage(driver)
    if assigned_or_unassigned == "assigned":
        assert countries_page.all_selected()
    else:
        assert countries_page.all_deselected()


@when("I click on the goods link from overview")  # noqa
def click_goods_link_overview(driver):  # noqa
    overview_page = GenericApplicationTaskListPage(driver)
    overview_page.click_goods_type_link()


@when("I create an open application")  # noqa
def create_open_app(driver, context):  # noqa
    click_apply_licence(driver)
    ApplyForALicencePage(driver).select_licence_type("export_licence")
    functions.click_submit(driver)
    enter_type_of_application(driver, "open", context)
    enter_application_name(driver, context)
    enter_permanent_or_temporary(driver, "permanent", context)


@given("I create an open application via api")
def open_application_exists(apply_for_open_application):
    pass


@when("I remove a good type from the application")
def i_remove_a_good_from_the_application(driver):
    remove_good_link = GenericApplicationTaskListPage(driver).find_remove_goods_type_link()
    driver.execute_script("arguments[0].click();", remove_good_link)


@then("no goods types are left on the application")
def no_goods_types_are_left_on_the_application(driver):
    assert (OpenApplicationGoodsTypesPage(driver).find_remove_goods_type_link(), None)


@when("I click on open goods tile")  # noqa
def click_my_goods_link(driver):  # noqa
    exporter_hub = GenericApplicationTaskListPage(driver)
    exporter_hub.click_goods_type_link()
