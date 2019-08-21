from pytest_bdd import when, then, parsers, scenarios, given

from pages.shared import Shared
from pages.submitted_applications_page import SubmittedApplicationsPages

import helpers.helpers as utils

scenarios('../features/switch_organisations.feature', strict_gherkin=False)


@given("I have a second set up organisation")
def set_up_second_organisation(register_organisation_for_switching_organisation):
    pass


@when("I switch organisations to my second organisation")
def switch_organisations_to_my_second_organisation(driver):
    driver.find_element_by_id('switch-link').click()
    driver.find_elements_by_css_selector('.govuk-radios__input')[1].click()
    Shared(driver).click_continue()


@then("I am on my second organisation names homepage")
def see_second_organisation_name(driver):
    assert driver.find_element_by_css_selector('.govuk-heading-xl').text == org_name_for_switching_organisations
