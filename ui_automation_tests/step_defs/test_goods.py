import os

from pytest_bdd import scenarios, when, then, parsers

from pages.attach_document_page import AttachDocumentPage
from pages.goods_list import GoodsList
from pages.exporter_hub_page import ExporterHubPage
from pages.add_goods_page import AddGoodPage
from pages.goods_page import GoodsPage
from pages.shared import Shared
from pages.application_overview_page import ApplicationOverviewPage

from ui_automation_tests.conftest import i_click_continue
from ui_automation_tests.pages.application_goods_list import ApplicationGoodsList


scenarios('../features/clc_queries_and_goods.feature', strict_gherkin=False)


@then('I see good in goods list')
def assert_good_is_in_list(driver, context, exporter_url):
    goods_list = GoodsList(driver)
    driver.get(exporter_url.rstrip('/') + '/goods/')
    goods_list.assert_goods_are_displayed_of_good_name(driver,
                                                       context.good_description,
                                                       context.part,
                                                       context.control_code)


@then('I see the clc query in goods list')
def assert_clc_is_in_list(driver, context, exporter_url):
    goods_list = GoodsList(driver)
    goods_list.assert_clc_goods_are_displayed_of_good_name(driver,
                                                           context.good_description,
                                                           context.part,
                                                           context.control_code)


@when(parsers.parse('I edit a good to description "{description}" controlled "{controlled}" '
                    'control code "{control_code}" incorporated "{incorporated}" and part number "{part}"'))
def edit_good(driver, description, controlled,  control_code, incorporated, part, context):
    exporter_hub = ExporterHubPage(driver)
    add_goods_page = AddGoodPage(driver)
    goods_list = GoodsList(driver)
    goods_list.select_a_draft_good()
    goods_page = GoodsPage(driver)
    goods_page.click_on_goods_edit_link()
    context.edited_description = context.good_description + " " + description
    add_goods_page.enter_description_of_goods(context.edited_description)
    exporter_hub.click_save_and_continue()


@then('I see my edited good in the goods list')
def see_my_edited_good_in_list(driver, context):
    assert context.edited_description in Shared(driver).get_text_of_gov_table()


@when('I delete my good')
def delete_my_good_in_list(driver, context):
    goods_page = GoodsPage(driver)
    goods_page.click_on_goods_edit_link()
    goods_page.click_on_delete_link()
    goods_page.confirm_delete(True)


@then('my good is no longer in the goods list')
def good_is_no_longer_in_list(driver, context):
    assert len(driver.find_elements_by_id('delete-' + context.good_id_from_url)) == 0


@when('I add a good and attach a document')
def attach_document_to_modifiable_good(driver, context, create_non_incorporated_good):
    pass


@then('I see the document has been attached')
def i_see_the_attached_good(driver, context):
    added_doc = AttachDocumentPage(driver).get_text_of_document_added_item()
    assert context.file_to_be_deleted_name in added_doc, "file is not displayed"
    assert context.document_description in added_doc, "file description is not displayed"


@then('I see my edited good details in the good page')
def click_on_draft_good(driver):
    text = driver.find_element_by_css_selector('.govuk-summary-list').text
    assert "edited" in text
    assert "Yes" in text
    assert "No" in text
    assert "321" in text


@when("I click to manage goods on a standard application")
def i_click_to_manage_goods_on_a_standard_application(driver):
    ApplicationOverviewPage(driver).click_standard_goods_link()


@then("I see there are no goods on the application")
def i_see_there_are_no_goods_on_the_application():
    pass


@when("I click Add a new good")
def i_click_add_a_new_good(driver):
    ApplicationGoodsList(driver).click_add_new_good_button()


@when(parsers.parse('I enter details for a good on an application with value "{value}", quantity "{quantity}" and unit of measurement "{unit}" and I click Continue"'))  # noqa
def i_enter_detail_for_the_good_on_the_application(driver, value, quantity, unit):
    ApplicationGoodsList(driver).add_values_to_good(value, quantity, unit)
    i_click_continue(driver)


@when(parsers.parse('I attach a document to the good with description "{description}"'))  # noqa
def i_attach_a_document_to_the_good(driver, description):
    file_to_be_deleted_name = 'file_for_doc_upload_test_2.txt'

    # Path gymnastics to get the absolute path for $PWD/../resources/(file_to_upload_x) that works everywhere
    file_to_upload_abs_path = \
        os.path.abspath(
            os.path.join(os.path.dirname(__file__), os.pardir, 'resources', file_to_be_deleted_name))
    if 'ui_automation_tests' not in file_to_upload_abs_path:
        file_to_upload_abs_path = \
            os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'ui_automation_tests/resources',
                                         file_to_be_deleted_name))

    attach_document_page = AttachDocumentPage(driver)
    attach_document_page.choose_file(file_to_upload_abs_path)
    attach_document_page.enter_description(description)
    Shared(driver).click_continue()


@then("A new good has been added to the application")
def a_new_good_has_been_added_to_the_application(driver):
    assert ApplicationGoodsList(driver).get_goods_count() == 1
