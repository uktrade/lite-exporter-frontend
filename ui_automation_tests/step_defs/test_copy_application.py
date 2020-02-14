from pytest_bdd import when, parsers, then, scenarios

from ui_automation_tests.pages.application_page import ApplicationPage
from ui_automation_tests.pages.apply_for_a_licence_page import ApplyForALicencePage
from ui_automation_tests.pages.generic_application.task_list import GenericApplicationTaskListPage
from ui_automation_tests.shared import functions

scenarios("../features/copy_application.feature", strict_gherkin=False)


@when("I click copy application")
def click_on_an_application(driver):
    ApplicationPage(driver).click_copy_application()


@when(parsers.parse('I add a name "{name}", and select "{option}" to being referred with code "{code}"'))
def enter_details_of_copied_application(driver, context, name, option, code):
    ApplyForALicencePage(driver).enter_name_or_reference_for_application(name)
    functions.click_submit(driver)
    ApplyForALicencePage(driver).click_export_licence_yes_or_no(option)
    ApplyForALicencePage(driver).type_into_reference_number(code)
    context.name = name
    context.reference_code = code
    functions.click_submit(driver)


@then("I see my new name added")
def name_is_defined(driver, context):
    assert context.name in GenericApplicationTaskListPage(driver).get_text_of_lite_task_list_items()


@then("I see the new reference code added")
def reference_code_added(driver, context):
    assert context.reference_code in GenericApplicationTaskListPage(driver).get_text_of_lite_task_list_items()


@then("the application contains products")
def products_are_listed(driver):
    assert "done" == GenericApplicationTaskListPage(driver).get_good_section_status()


@then("the application contains end users")
def end_users_are_listed(driver):
    assert "in-progress" == GenericApplicationTaskListPage(driver).get_end_user_section_status()


@then("the application contains consignees")
def consignees_are_listed(driver):
    assert "in-progress" == GenericApplicationTaskListPage(driver).get_consignee_section_status()


@then("the application contains third parties")
def third_parties_are_listed(driver):
    assert "done" == GenericApplicationTaskListPage(driver).get_third_parties_section_status()


@then("I see no supporting documents on the application")
def supporting_documents_not_included(driver):
    assert "other" == GenericApplicationTaskListPage(driver).get_supporting_documents_section_status()
