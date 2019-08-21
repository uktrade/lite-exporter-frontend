from pytest_bdd import when, then, scenarios, given

from pages.hub_page import Hub
from pages.shared import Shared

scenarios('../features/switch_organisations.feature', strict_gherkin=False)


@given("I have a second set up organisation")
def set_up_second_organisation(register_organisation_for_switching_organisation):
    pass


@when("I switch organisations to my second organisation")
def switch_organisations_to_my_second_organisation(driver):
    Hub(driver).click_switch_link()
    Shared(driver).click_on_radio_buttons(1)
    Shared(driver).click_continue()


@then("I am on my second organisation names homepage")
def see_second_organisation_name(driver, context):
    assert Shared(driver).get_text_of_heading() == context.org_name_for_switching_organisations
