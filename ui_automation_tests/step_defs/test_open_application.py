from pytest_bdd import scenarios, when, then, parsers, given

import ui_automation_tests.shared.tools.helpers as utils
from ui_automation_tests.pages.open_application.country_contract_types import OpenApplicationCountryContractTypes
from ui_automation_tests.pages.open_application.country_contract_types_summary import (
    OpenApplicationCountryContractTypesSummaryPage,
)
from ui_automation_tests.pages.exporter_hub_page import ExporterHubPage
from ui_automation_tests.pages.generic_application.ultimate_end_users import GenericApplicationUltimateEndUsers
from ui_automation_tests.shared import functions
from ui_automation_tests.conftest import (
    enter_type_of_application,
    enter_application_name,
    enter_permanent_or_temporary,
    choose_open_licence_category,
    answer_firearms_question,
)
from ui_automation_tests.pages.apply_for_a_licence_page import ApplyForALicencePage
from ui_automation_tests.pages.open_application.countries import OpenApplicationCountriesPage
from ui_automation_tests.pages.open_application.goods_countries_page import GoodsCountriesPage
from ui_automation_tests.pages.open_application.goods_types import OpenApplicationGoodsTypesPage
from ui_automation_tests.pages.standard_application.goods import StandardApplicationGoodsPage

scenarios(
    "../features/submit_open_application.feature", "../features/edit_open_application.feature", strict_gherkin=False
)


@then(parsers.parse('I see my goods type added at position "{position}" with a description and a control code'))
def i_see_the_goods_types_list(driver, position, context):
    goods_type_page = OpenApplicationGoodsTypesPage(driver)
    good_type = goods_type_page.get_text_of_goods_type_info(int(position))
    assert context.good_description in good_type
    assert context.control_code in good_type


@then(parsers.parse("I see a list of the preselected media products"))
def i_see_the_goods_types_list_media_oiel(driver, context):
    goods_type_page = OpenApplicationGoodsTypesPage(driver)
    goods_types = goods_type_page.get_number_of_goods()
    assert len(goods_types) == 7


@then(parsers.parse("I see a list of the preselected cryptographic products"))
def i_see_the_goods_types_list_cryptographic_oiel(driver, context):
    goods_type_page = OpenApplicationGoodsTypesPage(driver)
    goods_types = goods_type_page.get_number_of_goods()
    assert len(goods_types) == 4


@then("I should see a list of countries")
def i_should_see_a_list_of_countries(driver):
    application_countries_list = OpenApplicationCountriesPage(driver)
    page_countries = application_countries_list.get_countries_names()
    assert len(page_countries) == 274


@then("I should see a list of all countries that have been preselected")
def i_should_see_a_list_of_countries(driver):
    application_countries_list = OpenApplicationCountriesPage(driver)
    page_countries = application_countries_list.get_static_destinations_list()
    assert len(page_countries) == 274


@then("I should see a list of the countries permitted for a cryptographic OIEL")
def i_should_see_a_list_of_countries_cryptographic_oiel(driver):
    application_countries_list = OpenApplicationCountriesPage(driver)
    page_countries = application_countries_list.get_static_destinations_list()
    assert len(page_countries) == 213
    assert "United Kingdom" not in page_countries


@then("I should see the UK Continental Shelf as the only permitted destination")
def i_should_see_a_list_of_countries_uk_continental_shelf_oiel(driver):
    application_countries_list = OpenApplicationCountriesPage(driver)
    page_countries = application_countries_list.get_static_destinations_list()
    assert len(page_countries) == 1
    assert page_countries[0] == "UK Continental Shelf"


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


@when("I click select all countries")
def select_all_countries(driver):
    page = OpenApplicationCountriesPage(driver)
    page.click_select_all()


@then("all checkboxes are selected")
def all_selected(driver):
    page = OpenApplicationCountriesPage(driver)
    assert page.get_number_of_checkboxes(checked=False) == page.get_number_of_checkboxes(checked=True)


@when("I select that I want to add the same sectors and contract types to all countries")
def select_yes_to_all_countries_with_the_same_contract_types(driver):
    OpenApplicationCountryContractTypes(driver).select_same_contract_types_for_all_countries_radio_button()


@when("I select contract types for all countries")
def select_contract_types_for_all_countries(driver, context):
    page = OpenApplicationCountryContractTypes(driver)
    context.contract_types = ["Navy", "Aircraft manufacturers, maintainers or operators", "Pharmaceutical or medical"]
    page.select_contract_type(context.contract_types[0])
    page.select_contract_type(context.contract_types[1])
    page.select_contract_type(context.contract_types[2])
    page.select_other_contract_type_and_fill_in_details()
    functions.click_submit(driver)


@then("I should see all countries and the chosen contract types on the destination summary list")
def i_should_see_destinations_summary_countries_contract_types(driver, context):
    page = OpenApplicationCountryContractTypesSummaryPage(driver)
    countries_and_contract_types = page.get_countries_with_respective_contract_types()
    assert len(countries_and_contract_types) == 274
    for country_with_contract_types in countries_and_contract_types:
        for contract_type in context.contract_types:
            assert contract_type in country_with_contract_types[1]


@then(
    "I should see the UK Continental Shelf as the only destination and the chosen contract types on the destination summary list"
)
def i_should_see_destinations_summary_uk_continental_shelf_contract_types(driver, context):
    page = OpenApplicationCountryContractTypesSummaryPage(driver)
    countries_and_contract_types = page.get_countries_with_respective_contract_types()
    assert len(countries_and_contract_types) == 1
    assert countries_and_contract_types[0][0] == "UK Continental Shelf"
    for country_with_contract_types in countries_and_contract_types:
        for contract_type in context.contract_types:
            assert contract_type in country_with_contract_types[1]


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
    OpenApplicationGoodsTypesPage(driver).click_add_good_button()


@then(parsers.parse('I see all countries are "{assigned_or_unassigned}" to all goods'))
def see_all_or_no_selected(driver, assigned_or_unassigned):
    countries_page = GoodsCountriesPage(driver)
    if assigned_or_unassigned == "assigned":
        assert countries_page.all_selected()
    else:
        assert countries_page.all_deselected()


@when(parsers.parse('I create an open application of a "{export_type}" export type'))  # noqa
def create_open_app(driver, export_type, context):  # noqa
    ExporterHubPage(driver).click_apply_for_a_licence()
    ApplyForALicencePage(driver).select_licence_type("export_licence")
    functions.click_submit(driver)
    enter_type_of_application(driver, "oiel", context)
    choose_open_licence_category(driver, "military", context)
    enter_permanent_or_temporary(driver, export_type, context)
    enter_application_name(driver, context)
    answer_firearms_question(driver)


@when(parsers.parse('I create an open application for an export licence of the "{licence_type}" licence type'))  # noqa
def create_open_app_of_specific_type(driver, licence_type, context):  # noqa
    ExporterHubPage(driver).click_apply_for_a_licence()
    ApplyForALicencePage(driver).select_licence_type("export_licence")
    functions.click_submit(driver)
    enter_type_of_application(driver, "oiel", context)
    choose_open_licence_category(driver, licence_type, context)

    if licence_type in ["military", "uk_continental_shelf"]:
        enter_permanent_or_temporary(driver, "permanent", context)

    enter_application_name(driver, context)
    if licence_type in ["military", "uk_continental_shelf"]:
        answer_firearms_question(driver)


@when("I click on the add button")
def i_click_on_the_add_button(driver):
    GenericApplicationUltimateEndUsers(driver).click_add_ultimate_recipient_button()


@when("I remove a good type from the application")
def i_remove_a_good_from_the_application(driver):
    remove_good_link = StandardApplicationGoodsPage(driver).find_remove_goods_type_link()
    driver.execute_script("arguments[0].click();", remove_good_link)


@then("no goods types are left on the application")
def no_goods_types_are_left_on_the_application(driver):
    assert (OpenApplicationGoodsTypesPage(driver).find_remove_goods_type_link(), None)
