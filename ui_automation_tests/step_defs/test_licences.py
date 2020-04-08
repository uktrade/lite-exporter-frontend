from pytest_bdd import scenarios, given, parsers, when, then

from ui_automation_tests.pages.licences_page import LicencesPage
from ui_automation_tests.shared.tools.helpers import find_paginated_item_by_id

scenarios("../features/licences.feature", strict_gherkin=False)


@given(parsers.parse('I create "{decision}" final advice for open application'))
def final_advice_open(context, decision, api_test_client):
    api_test_client.cases.create_final_advice(
        context.case_id, [{"type": decision, "text": "abc", "note": "", "goods_type": context.goods_type["id"]}]
    )


@when("I go to the licences page")
def licences_page(driver, exporter_url):
    driver.get(exporter_url.rstrip("/") + "/licences/")


@then("I see my standard licence")
def standard_licence_row(context, driver):
    find_paginated_item_by_id(LicencesPage.LICENCE_ROW_PARTIAL_ID + context.licence, driver)
    row = LicencesPage(driver).licence_row_properties(context.licence)
    assert context.reference_code in row
    assert context.good["good"]["control_code"] in row
    assert context.good["good"]["description"] in row
    assert context.end_user["country"]["name"] in row
    assert context.end_user["name"] in row
    assert "Finalised" in row


@then("I see my open licence")
def open_licence_row(context, driver):
    find_paginated_item_by_id(LicencesPage.LICENCE_ROW_PARTIAL_ID + context.licence, driver)
    row = LicencesPage(driver).licence_row_properties(context.licence)
    assert context.reference_code in row
    assert context.goods_type["control_code"] in row
    assert context.goods_type["description"] in row
    assert context.country["name"] in row
    assert "Finalised" in row


@when("I click on the clearances tab")
def clearances_tab(driver):
    LicencesPage(driver).click_clearances_tab()


@then("I see my exhibition licence")
def exhibition_licence_row(context, driver):
    find_paginated_item_by_id(LicencesPage.LICENCE_ROW_PARTIAL_ID + context.licence, driver)
    row = LicencesPage(driver).licence_row_properties(context.licence)
    assert context.reference_code in row
    assert context.good["good"]["control_code"] in row
    assert context.good["good"]["description"] in row
    assert "Finalised" in row


@when("I click on the nlr tab")
def nlr_tab(driver):
    LicencesPage(driver).click_nlr_tab()