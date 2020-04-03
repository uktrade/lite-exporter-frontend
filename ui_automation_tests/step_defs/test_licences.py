from pytest_bdd import scenarios, given, parsers, when, then

from ui_automation_tests.pages.licences_page import LicencesPage
from ui_automation_tests.shared.tools.helpers import find_paginated_item_by_id

scenarios("../features/licences.feature", strict_gherkin=False)


@given(parsers.parse("I create a licence for my application"))
def create_licence(context, api_test_client):
    api_test_client.cases.finalise_case(context.case_id, "approve")
    api_test_client.cases.finalise_licence(context.case_id)
    context.licence = api_test_client.context["licence"]


@when("I go to the licences page")
def licences_page(driver, exporter_url):
    driver.get(exporter_url.rstrip("/") + "/licences/")


@then("I see my standard licence")
def licence_row(context, driver):
    licences_page = LicencesPage(driver)
    find_paginated_item_by_id(licences_page.LICENCE_ROW_PARTIAL_ID + context.licence, driver)
    row = licences_page.licence_row_properties(context.licence)
    assert context.reference_code in row
    assert context.good["good"]["control_code"] in row
    assert context.good["good"]["description"] in row
    assert str(context.good["quantity"]) in row
    assert context.end_user["country"]["name"] in row
    assert context.end_user["name"] in row
    assert "Finalised" in row
