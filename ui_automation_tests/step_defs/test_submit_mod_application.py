from pytest_bdd import scenarios, when, parsers, then

from ui_automation_tests.pages.apply_for_a_licence_page import ApplyForALicencePage
from ui_automation_tests.pages.generic_application.task_list import GenericApplicationTaskListPage
from ui_automation_tests.pages.mod_clearances.ExhibitionClearanceDetails import ExhibitionClearanceDetailsPage
from ui_automation_tests.pages.mod_clearances.ExhibitionClearanceGood import ExhibitionClearanceGoodPage
from ui_automation_tests.pages.shared import Shared
from ui_automation_tests.pages.standard_application.good_details import StandardApplicationGoodDetails
from ui_automation_tests.pages.standard_application.goods import StandardApplicationGoodsPage
from ui_automation_tests.shared import functions

scenarios("../features/submit_mod_application.feature", strict_gherkin=False)


@when(parsers.parse('I select a MOD licence of type "{type}"'))  # noqa
def create_mod_application(driver, context, type):  # noqa
    ApplyForALicencePage(driver).select_mod_application_type(type)
    functions.click_submit(driver)


@then("The Exhibition details section is complete")
def exhibition_details_done(driver):
    GenericApplicationTaskListPage(driver).check_exhibition_details_section_status("done")


@when("I add a good to the Exhibition Clearance")  # noqa
def i_add_a_non_incorporated_good_to_the_application(driver, context):  # noqa
    goods_page = StandardApplicationGoodsPage(driver)
    goods_page.click_add_preexisting_good_button()
    goods_page.click_add_to_application()

    # Enter good details
    context.good_type = "equipment"
    ExhibitionClearanceGoodPage(driver).click_good_type(context.good_type)
    functions.click_submit(driver)


@then("the good is added to the Exhibition Clearance")  # noqa
def the_good_is_added_to_the_application(driver, context):  # noqa
    assert len(StandardApplicationGoodsPage(driver).get_goods()) == 1  # Only one good added
    assert context.good_type in Shared(driver).get_table_row(1).text

    # Go back to task list
    functions.click_back_link(driver)
