from pytest_bdd import scenarios, then, when, parsers, given

from pages.shared import Shared
from ui_automation_tests.pages.application_page import ApplicationPage
from ui_automation_tests.pages.submitted_applications_page import SubmittedApplicationsPages
from ui_automation_tests.shared.functions import element_with_id_exists

scenarios("../features/withdraw_and_surrender_application.feature", strict_gherkin=False)

RADIO_BUTTONS = "[type='radio']"


@when("I click the button 'Withdraw Application'")
def i_click_withdraw_application(driver):
    ApplicationPage(driver).click_withdraw_application_button()


@when("I click the button 'Surrender Application'")
def i_click_withdraw_application(driver):
    ApplicationPage(driver).click_surrender_application_button()


@then("I should see a confirmation page")
def i_should_see_a_confirmation_page(driver):
    assert len(driver.find_elements_by_css_selector(RADIO_BUTTONS)) == 2


@when("I select the yes radiobutton")
def i_select_the_yes_radiobutton(driver):
    driver.find_element_by_id("choice-yes").click()


@then(parsers.parse('the application will have the status "{status}"'))
def the_application_will_have_status(driver, status):
    assert ApplicationPage(driver).get_status() == status


@then("I won't be able to see the withdraw button")
def i_wont_be_able_to_see_the_withdraw_button(driver):
    text = Shared(driver).get_text_of_case_buttons()
    assert "Withdraw" not in text
    assert "Copy" in text


@then("I won't be able to see the surrender button")
def i_wont_be_able_to_see_the_surrender_button(driver):
    text = Shared(driver).get_text_of_case_buttons()
    assert "Surrender" not in text
    assert "Copy" in text


@then("the edit application button is not present")
def edit_button_not_present(driver):
    text = Shared(driver).get_text_of_case_buttons()
    assert "Edit" not in text


@then("the case note text area is not present")
def edit_button_not_present(driver):
    text = Shared(driver).get_text_of_main_content()
    assert "Post note" not in text
    assert "Cancel" not in text
    assert "Add a note" not in text
