from pytest_bdd import scenarios, when, parsers, then

from ui_automation_tests.pages.apply_for_a_licence_page import ApplyForALicencePage
from ui_automation_tests.shared import functions

scenarios("../features/submit_mod_application.feature", strict_gherkin=False)


@when(parsers.parse('I select a MOD licence of type "{type}"'))  # noqa
def create_mod_application(driver, context, type):  # noqa
    ApplyForALicencePage(driver).select_mod_application_type(type)
    functions.click_submit(driver)


@when("I choose types of clearance I need")
def choose_types_of_clearance(driver):
    ApplyForALicencePage(driver).select_types_of_clearance()
    functions.click_submit(driver)


@then("I see the correct number of clearance types")
def correct_number_of_types(driver):
    assert len(driver.find_elements_by_name(ApplyForALicencePage(driver).F680_CLEARANCE_TYPE_CHECKBOXES_NAME)) == 6
