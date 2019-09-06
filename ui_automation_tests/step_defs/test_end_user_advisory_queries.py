from pytest_bdd import when, then, given, parsers, scenarios

from pages.add_end_user_advisory_pages import AddEndUserAdvisoryPages
from pages.exporter_hub_page import ExporterHubPage
from pages.end_user_advisory_page import EndUserAdvisoryPage

scenarios('../features/end_user_advisory_queries.feature', strict_gherkin=False)


@when('I select to create a new advisory')
def apply_for_end_user_advisory(driver):
    enduseradvisorypage = EndUserAdvisoryPage(driver)
    enduseradvisorypage.apply_for_advisory()


@when(parsers.parse('I select "{type}" option and continue'))
def select_end_user_type(driver, type):
    enduserpage = AddEndUserAdvisoryPages(driver)
    enduserpage.select_type(type)
    enduserpage.click_continue()


@when(parsers.parse('I select "{name}" for the name, "{address}" for the address, "{country}" as the country, and continue'))
def add_user_details(driver, name, address, country):
    enduserpage = AddEndUserAdvisoryPages(driver)
    enduserpage.enter_name(name)
    enduserpage.enter_address(address)
    enduserpage.enter_country(country)
    enduserpage.click_continue()


@when(parsers.parse('I enter "{reasoning}" for my reason, and "{notes}" for notes and click submit'))
def enter_advisory_details(driver, reasoning, notes):
    enduserpage = AddEndUserAdvisoryPages(driver)
    enduserpage.enter_reasoning(reasoning)
    enduserpage.enter_notes(notes)
    enduserpage.click_continue()


@then('I am given a confirmed submitted page, and am shown a 10 digit code')
def confirm_submitted_page_code(driver):
    enduserpage = AddEndUserAdvisoryPages(driver)
    enduserpage.confirmation_code()
    assert len(enduserpage.confirmation_code()) == 10
