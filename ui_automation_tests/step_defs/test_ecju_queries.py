from pytest_bdd import when, then, given, parsers, scenarios
from pages.application_page import ApplicationPage
from pages.respond_to_ecju_query_page import RespondToEcjuQueryPage

import helpers.helpers as utils

scenarios('../features/ecju_queries.feature', strict_gherkin=False)


@given('An application exists and a ecju query has been added via internal gov site')
def application_exists_ecju_query_added(add_an_application, internal_ecju_query):
    pass


@when('I click on an application previously created')
def click_on_an_application(driver, add_an_application):
    driver.refresh()
    elements = driver.find_elements_by_css_selector('a[href*="/applications/"]')
    elements[len(elements)-1].click()


@when('I select to view ecju queries')
def click_ecju_query_tab(driver, add_an_application):
    application_page = ApplicationPage(driver)
    application_page.click_ecju_query_tab()


# @then('I see the correct amount of ecju notifications')
# def compare_open_ecju_queries_with_bubble(driver):
#     application_page = ApplicationPage(driver)
#     open_queries = application_page.get_count_of_open_ecju_queries()
#     bubble_value = application_page.get_bubble_value('ECJU Queries')
#     assert open_queries == bubble_value


@when('I click to respond to the ecju query')
def click_ecju_query_tab(driver, add_an_application):
    application_page = ApplicationPage(driver)
    application_page.respond_to_ecju_query(0)


@when(parsers.parse('I enter "{response}" for ecju query and click submit'))
def respond_to_query(driver, response):
    response_page = RespondToEcjuQueryPage(driver)
    response_page.enter_form_response(response)
    response_page.click_submit()


@then('I see my ecju query is closed')
def compare_open_ecju_queries_with_bubble(driver):
    application_page = ApplicationPage(driver)
    closed_queries = application_page.get_count_of_closed_ecju_queries()
    assert closed_queries > 0
