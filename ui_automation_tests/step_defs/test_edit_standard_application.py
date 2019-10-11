from pytest_bdd import when, scenarios, then

from pages.application_overview_page import ApplicationOverviewPage
from pages.application_page import ApplicationPage

scenarios('../features/edit_standard_application.feature', strict_gherkin=False)


@when("I remove all goods on the application")
def i_remove_all_goods_on_the_application(driver):
    """
    Recursively removes all goods listed on the page, if any
    """
    remove_good_link = ApplicationOverviewPage(driver).find_remove_good_link()

    if remove_good_link:
        driver.execute_script("arguments[0].click();", remove_good_link)
        i_remove_all_goods_on_the_application(driver)


@then("No goods are left on the application")
def no_goods_are_left_on_the_application(driver):
    assert(ApplicationOverviewPage(driver).find_remove_good_link(), None)
