from pytest_bdd import when, scenarios, then, given

from pages.application_overview_page import ApplicationOverviewPage

scenarios('../features/edit_open_application.feature', strict_gherkin=False)


@given('an open application exists')
def open_application_exists(add_an_open_application):
    pass


@when('I click on an open application previously created')
def click_on_an_open_application(driver, context):
    driver.find_element_by_partial_link_text(context.open_app_name).click()


@when("I remove all goods types on the application")
def i_remove_all_goods_types_on_the_application(driver):
    """
    Recursively removes all goods types listed on the page, if any
    """
    remove_goods_type_link = ApplicationOverviewPage(driver).find_remove_goods_type_link()

    if remove_goods_type_link:
        driver.execute_script("arguments[0].click();", remove_goods_type_link)
        i_remove_all_goods_types_on_the_application(driver)


@then("No goods types are left on the application")
def no_goods_types_are_left_on_the_application(driver):
    assert(ApplicationOverviewPage(driver).find_remove_goods_type_link(), None)
