from pytest_bdd import when, then, parsers, scenarios, given

from pages.add_end_user_advisory_pages import AddEndUserAdvisoryPages
from pages.end_user_advisory_page import EndUserAdvisoryPage
from pages.respond_to_ecju_query_page import RespondToEcjuQueryPage
from pages.shared import Shared

from core.builtins.custom_tags import reference_code
from ui_automation_tests.helpers import helpers
from ui_automation_tests.pages.application_page import ApplicationPage
from ui_automation_tests.pages.submitted_applications_page import SubmittedApplicationsPages

scenarios('../features/end_user_advisory_queries.feature', strict_gherkin=False)


@given('an end user advisory with a case note has been added via gov user')
def end_user_advisory_exists_case_note_added(driver, add_end_user_advisory, internal_case_note, context):
    pass

@given('an end user advisory with an ecju query has been added via gov user')
def end_user_advisory_exists_ecju_query_added(driver, add_end_user_advisory, internal_ecju_query, context):
    pass

@when('I select to create a new advisory')
def apply_for_end_user_advisory(driver):
    end_user_advisory_page = EndUserAdvisoryPage(driver)
    end_user_advisory_page.click_apply_for_advisories()
    Shared(driver).click_continue()


@when(parsers.parse('I select "{type}" user type and continue'))
def select_end_user_type(driver, type):
    end_user_page = AddEndUserAdvisoryPages(driver)
    prefix = "end_user."
    end_user_page.select_type(type, prefix)
    Shared(driver).click_continue()


@when(parsers.parse('I enter "{name}" for the name'))
def add_user_details(driver, name):
    end_user_page = AddEndUserAdvisoryPages(driver)
    prefix = "end_user."
    end_user_page.enter_name(name, prefix)
    Shared(driver).click_continue()


@when(parsers.parse('I enter "{nature}" for the nature of business'))
def add_user_details(driver, nature):
    end_user_page = AddEndUserAdvisoryPages(driver)
    end_user_page.enter_nature(nature)
    Shared(driver).click_continue()


@when(parsers.parse('I enter "{name}" for the primary contact name, "{job}" for primary contact_job_title, "{email}" for the primary contact email, "{telephone}" for the primary contact telephone'))
def add_user_details(driver, name, email, telephone, job):
    end_user_page = AddEndUserAdvisoryPages(driver)
    end_user_page.enter_primary_contact_email(email)
    end_user_page.enter_primary_contact_name(name)
    end_user_page.enter_primary_contact_job_title(job)
    end_user_page.enter_primary_contact_telephone(telephone)
    Shared(driver).click_continue()


@when(parsers.parse('I enter "{address}" for the address, "{country}" as the country and continue'))
def add_user_details(driver, address, country):
    end_user_page = AddEndUserAdvisoryPages(driver)
    prefix = "end_user."
    end_user_page.enter_address(address, prefix)
    end_user_page.enter_country(country, prefix)
    Shared(driver).click_continue()


@when(parsers.parse('I enter "{reasoning}" for my reason, and "{notes}" for notes and click submit'))
def enter_advisory_details(driver, reasoning, notes):
    end_user_page = AddEndUserAdvisoryPages(driver)
    end_user_page.enter_reasoning(reasoning)
    end_user_page.enter_notes(notes)
    Shared(driver).click_continue()


@then('I am given a confirmed submitted page, and am shown a 10 digit code')
def confirm_submitted_page_code(driver):
    end_user_page = AddEndUserAdvisoryPages(driver)
    assert len(end_user_page.confirmation_code()) == 10


@when("I click copy on an existing end user advisory")
def click_copy(driver):
    driver.find_elements_by_link_text('Copy')[0].click()


@when(parsers.parse('I enter "{name}" for the name and continue'))
def enter_name(driver, name):
    prefix = "end_user."
    AddEndUserAdvisoryPages(driver).enter_name(name, prefix)
    Shared(driver).click_continue()


@when('I open an end user advisory already created')
def open_already_created_end_user_advisory(driver, context):
    elements = driver.find_elements_by_css_selector(".govuk-table__row")
    no = helpers.get_element_index_by_partial_text(elements, reference_code(context.end_user_advisory_id))
    elements[no].find_elements_by_css_selector("a")[0].click()


@then('I see a notification on end user advisory list')
def notification_on_end_user_advisory_list(driver, context):
    elements = driver.find_elements_by_css_selector(".govuk-table__row")
    no = helpers.get_element_index_by_partial_text(elements, reference_code(context.end_user_advisory_id))
    assert elements[no].find_element_by_css_selector(Shared(driver).notification).is_displayed()


@then('I see a notification for case note and can view the case note')
def notification_on_notes_tab(driver):
    tab = driver.find_element_by_id('case-notes-tab')
    assert tab.find_element_by_css_selector('.lite-notification-bubble').text == '1'
    assert 'I Am Easy to Find' in driver.find_elements_by_css_selector(".lite-application-note")[0].text


@then(parsers.parse('I can view "{text}" in case notes'))
def notification_on_notes_tab(driver, text):
    assert text in driver.find_elements_by_css_selector(".lite-application-note")[0].text


@when(parsers.parse('I enter "{text}" for case note'))
def enter_case_note_text(driver, text):
    application_page = SubmittedApplicationsPages(driver)
    application_page.enter_case_note(text)
    application_page.click_post_note_btn()


@when('I select to view ecju queries')
def click_ecju_query_tab(driver):
    application_page = ApplicationPage(driver)
    application_page.click_ecju_query_tab()


@when('I click to respond to the ecju query')
def click_ecju_query_tab(driver):
    application_page = ApplicationPage(driver)
    application_page.respond_to_ecju_query(0)


@when(parsers.parse('I enter "{response}" for ecju query and click submit'))
def respond_to_query(driver, response):
    response_page = RespondToEcjuQueryPage(driver)
    response_page.enter_form_response(response)
    Shared(driver).click_continue()


@when(parsers.parse('I select "{value}" for submitting response and click submit'))
def submit_response_confirmation(driver, value):
    driver.find_element_by_xpath('//input[@value="' + value + '"]').click()
    driver.find_element_by_xpath('//button[@type="submit"]').click()


@then('I see my ecju query is closed')
def determine_that_there_is_a_closed_query(driver):
    application_page = ApplicationPage(driver)
    closed_queries = application_page.get_count_of_closed_ecju_queries()
    assert closed_queries > 0