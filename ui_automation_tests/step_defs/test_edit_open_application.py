from pytest_bdd import when, scenarios, then, given

from ui_automation_tests.pages.application_goods_type_list import ApplicationGoodsTypeList

scenarios('../features/edit_open_application.feature', strict_gherkin=False)


@given('I create an open application via api')
def open_application_exists(apply_for_open_application):
    pass


@when("I remove all goods types on the application")
def i_remove_all_goods_types_on_the_application(driver):
    """
    Recursively removes all goods types listed on the page, if any
    """
    remove_goods_type_link = ApplicationGoodsTypeList(driver).find_remove_goods_type_link()

    if remove_goods_type_link:
        driver.execute_script("arguments[0].click();", remove_goods_type_link)
        i_remove_all_goods_types_on_the_application(driver)


@then("no goods types are left on the application")
def no_goods_types_are_left_on_the_application(driver):
    assert(ApplicationGoodsTypeList(driver).find_remove_goods_type_link(), None)
