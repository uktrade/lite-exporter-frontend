import time

from pytest_bdd import scenarios, when, then, parsers

import helpers.helpers as utils
from pages.add_end_user_pages import AddEndUserPages
from pages.application_overview_page import ApplicationOverviewPage
from pages.shared import Shared
from pages.application_goods_list import ApplicationGoodsList
from pages.ultimate_end_users_list_page import UltimateEndUsersListPage

scenarios('../features/submit_standard_application.feature', strict_gherkin=False)


@when('I click on application overview')
def i_click_on_application_overview(driver):
    Shared(driver).click_on_application_name()


@then('good is added to application')
def good_is_added(driver, context):
    good = ApplicationOverviewPage(driver).get_text_of_good(1)
    assert context.goods_name in good
    assert context.part_number in good
    # TODO put this back when bug is fixed - showing mtr instead of metres
    assert str(context.quantity) + ".0" in good
    assert context.unit in good
    if "." not in context.value:
        assert '£' + str(context.value) + '.00' in good
    else:
        assert '£' + str(context.value) in good


@then('I see the homepage')
def i_see_the_homepage(driver):
    assert 'Exporter hub - LITE' in driver.title, "Delete Application link on overview page failed to go to Exporter Hub page"


@when('I click on ultimate end users')
def i_click_on_application_overview(driver, add_an_incorporated_good_to_application):
    app = ApplicationOverviewPage(driver)
    app.click_ultimate_end_user_link()


@when('I click on back to overview')
def i_go_to_the_overview(driver):
    app = ApplicationOverviewPage(driver)
    app.click_on_back_to_overview_text()


@when('I click on ultimate end users add button')
def i_click_on_ultimate_end_user(driver):
    UltimateEndUsersListPage(driver).click_on_add_ultimate_end_user()


@when(parsers.parse('I add end user of type: "{type}"'))
def add_new_end_user_type(driver, type, context):
    add_end_user_pages = AddEndUserPages(driver)
    add_end_user_pages.select_type(type)
    context.type_end_user = type
    add_end_user_pages.click_continue()


@when(parsers.parse('I add end user of name: "{name}"'))
def add_new_end_user_name(driver, name, context):
    add_end_user_pages = AddEndUserPages(driver)
    add_end_user_pages.enter_name(name)
    context.name_end_user = name
    add_end_user_pages.click_continue()


@when(parsers.parse('I add end user of website "{website}"'))
def add_new_end_user_website(driver, website):
    add_end_user_pages = AddEndUserPages(driver)
    add_end_user_pages.enter_website(website)
    add_end_user_pages.click_continue()


@when(parsers.parse('I add end user of address: "{address}" and country "{country}"'))
def add_new_end_user_address(driver, address, country, context):
    add_end_user_pages = AddEndUserPages(driver)
    add_end_user_pages.enter_address(address)
    context.address_end_user = address
    add_end_user_pages.enter_country(country)
    add_end_user_pages.click_continue()


@when('I remove an ultimate end user so there is one less and return to the overview')
def i_remove_an_ultimate_end_user(driver):
    no_of_ultimate_end_users = Shared(driver).get_size_of_table_rows()
    driver.find_element_by_link_text('Remove').click()
    total = no_of_ultimate_end_users - Shared(driver).get_size_of_table_rows()
    assert total == 1, "total on the ultimate end users summary is incorrect after removing ultimate end user"
    app = ApplicationOverviewPage(driver)
    app.click_on_back_to_overview_text()


@then('there is only one ultimate end user')
def one_ultimate_end_user(driver):
    elements = Shared(driver).get_lite_sections()
    no = utils.get_element_index_by_partial_text(elements, "Ultimate End Users")
    assert len(elements[no].find_elements_by_css_selector(".govuk-table__row")) == 2, "total on the application overview is incorrect after removing ultimate end user"


@then("I see no goods and external sites error message")
def i_see_no_sites_attached_error(driver):
    shared = Shared(driver)
    assert "Cannot create an application with no goods attached" in shared.get_text_of_error_messages()
    assert "Cannot create an application with no sites or external sites attached" in shared.get_text_of_error_messages()


@then('I see no ultimate end user attached error message')
def i_see_no_ultimate_end_user_attached_error(driver):
    shared = Shared(driver)
    assert "Cannot create an application with no ultimate end users set when " \
           "there is a good which is to be incorporated into an end product" in shared.get_text_of_error_messages()


@then('I see end user on overview')
def end_user_on_overview(driver, context):
    app = ApplicationOverviewPage(driver)
    assert "Type" in app.get_text_of_end_user_table()
    assert "Name" in app.get_text_of_end_user_table()
    assert "Address" in app.get_text_of_end_user_table()
    assert context.type_end_user in app.get_text_of_end_user_table()
    assert context.name_end_user in app.get_text_of_end_user_table()
    assert context.address_end_user in app.get_text_of_end_user_table()


@then('I see enter valid quantity and valid value error message')
def valid_quantity_value_error_message(driver):
    shared = Shared(driver)
    assert "A valid number is required." in shared.get_text_of_error_messages()
    assert "Enter a valid quantity" in shared.get_text_of_error_messages()
    assert "Select a unit" in shared.get_text_of_error_messages()


@when(parsers.parse('I click add to application for the good at position "{no}"'))
def click_add_to_application_button(driver, no, context):
    num = int(no) - 1
    context.goods_name = ApplicationGoodsList(driver).get_text_of_gov_heading_within_card(num)
    context.part_number = ApplicationGoodsList(driver).get_text_of_part_number(num)
    driver.find_elements_by_css_selector('a.govuk-button')[num].click()


@when(parsers.parse(
    'I add an end user of type: "{type}", name: "{name}", website: "{website}", address: "{address}" and country "{country}"'))
def add_new_end_user(driver, type, name, website, address, country, context):
    add_end_user_pages = AddEndUserPages(driver)
    add_end_user_pages.select_type(type)
    context.type_end_user = type
    add_end_user_pages.click_continue()
    add_end_user_pages.enter_name(name)
    context.name_end_user = name
    add_end_user_pages.click_continue()
    add_end_user_pages.enter_website(website)
    add_end_user_pages.click_continue()
    add_end_user_pages.enter_address(address)
    context.address_end_user = address
    add_end_user_pages.enter_country(country)
    add_end_user_pages.click_continue()


@when('I click on end user')
def i_click_on_end_user(driver):
    app = ApplicationOverviewPage(driver)
    app.click_end_user_link()


@when('I add a non incorporated good to application')
def add_a_non_incorporated_good(driver, add_a_non_incorporated_good_to_application):
    pass


@when("I wait for the end user document to be processed")
def i_wait_for_end_user_document_to_be_processed(driver):
    app = ApplicationOverviewPage(driver)
    # Constants for total time to retry function and intervals between attempts
    timeout_limit = 20
    function_retry_interval = 1

    time_no = 0
    while time_no < timeout_limit:
        if "Download" in app.get_end_user_document_state_text():
            return True
        time.sleep(function_retry_interval)
        time_no += function_retry_interval
        driver.refresh()
    return False
