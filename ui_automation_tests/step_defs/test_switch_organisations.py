from pytest_bdd import then, scenarios
from ui_automation_tests.pages.shared import Shared

scenarios("../features/switch_organisations.feature", strict_gherkin=False)


@then("I am on my second organisation names homepage")
def see_second_organisation_name(driver, context):
    assert Shared(driver).get_text_of_organisation_heading() == context.org_name_for_switching_organisations
