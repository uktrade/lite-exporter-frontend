from pytest_bdd import scenarios, given

from ui_automation_tests.shared import functions

scenarios("../features/edit_mod_application.feature", strict_gherkin=False)


def click_radio_button(driver, button_id):
    driver.find_element_by_id(button_id).click()

@given("I create a exhibition clearance application via api")  # noqa
def exhibition_clearance_exists(apply_for_exhibition_clearance):  # noqa
    pass


@given("I create a F680 clearance application via api")  # noqa
def f680_clearance_exists(apply_for_f680_clearance):  # noqa
    pass


@given("I create a gifting clearance application via api")  # noqa
def gifting_clearance_exists(apply_for_gifting_clearance):  # noqa
    pass


@when("I add additional information")
def add_new_additional_information(driver, context):  # noqa
    click_radio_button(driver, "expedited-True")
    functions.click_submit(driver)
    click_radio_button(driver, "foreign_technology-False")
    functions.click_submit(driver)
    click_radio_button(driver, "locally_manufactured-False")
    functions.click_submit(driver)
    click_radio_button(driver, "mtcr_type-mtcr_category_2")
    functions.click_submit(driver)
    click_radio_button(driver, "electronic_warfare_requirement-False")
    functions.click_submit(driver)
    click_radio_button(driver, "uk_service_equipment-False")
    functions.click_submit(driver)
    functions.click_submit(driver)
    functions.click_submit(driver, "finish")
