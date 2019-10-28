from pytest_bdd import when, scenarios, then

from pages.application_overview_page import ApplicationOverviewPage
from pages.shared import Shared

scenarios('../features/edit_standard_application.feature', strict_gherkin=False)


@when('I click back to the application overview')
def i_click_on_application_overview(driver):
    Shared(driver).click_back_link()


@when('I click on the application third parties link')
def i_click_on_application_third_parties_link(driver):
    ApplicationOverviewPage(driver).click_third_parties()


@when("I remove a third party from the application")
def i_remove_a_third_party_from_the_application(driver):
    remove_good_link = ApplicationOverviewPage(driver).find_remove_third_party_link()
    driver.execute_script("arguments[0].click();", remove_good_link)


@then("the third party has been removed from the application")
def no_third_parties_are_left_on_the_application(driver):
    assert(ApplicationOverviewPage(driver).find_remove_third_party_link(), None)


@when("I remove a good from the application")
def i_remove_a_good_from_the_application(driver):
    remove_good_link = ApplicationOverviewPage(driver).find_remove_good_link()
    driver.execute_script("arguments[0].click();", remove_good_link)


@then("the good has been removed from the application")
def no_goods_are_left_on_the_application(driver):
    assert(ApplicationOverviewPage(driver).find_remove_good_link(), None)


@when("I remove the end user off the application")
def i_remove_the_end_user_off_the_application(driver):
    remove_end_user_link = ApplicationOverviewPage(driver).find_remove_end_user_link()
    driver.execute_script("arguments[0].click();", remove_end_user_link)


@then("no end user is set on the application")
def no_end_user_is_set_on_the_application(driver):
    assert (ApplicationOverviewPage(driver).find_remove_end_user_link(), None)


@when("I remove the consignee off the application")
def i_remove_the_consignee_off_the_application(driver):
    remove_consignee_link = ApplicationOverviewPage(driver).find_remove_consignee_link()
    driver.execute_script("arguments[0].click();", remove_consignee_link)


@then("no consignee is set on the application")
def no_consignee_is_set_on_the_application(driver):
    assert (ApplicationOverviewPage(driver).find_remove_consignee_link(), None)


@when('I remove an additional document')
def i_remove_an_additional_document(driver):
    remove_consignee_link = ApplicationOverviewPage(driver).find_remove_additional_document_link()
    driver.execute_script("arguments[0].click();", remove_consignee_link)


@when('I confirm I want to delete the document')
def i_click_confirm(driver, add_an_incorporated_good_to_application):
    ApplicationOverviewPage(driver).confirm_delete_additional_document()


@then("the document is removed from the application")
def no_documents_are_set_on_the_application(driver):
    assert (ApplicationOverviewPage(driver).find_remove_additional_document_link(), None)