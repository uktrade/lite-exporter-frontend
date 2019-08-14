import datetime
import os
import allure
from allure_commons.types import AttachmentType

import pytest
from fixtures.core import context, driver, invalid_username, exporter_sso_login_info, s3_key
from fixtures.register_organisation import register_organisation
from fixtures.add_goods import add_a_good, add_an_incorporated_good_to_application, add_a_non_incorporated_good_to_application, create_non_incorporated_good
from fixtures.add_an_application import add_an_application
from fixtures.sso_sign_in import sso_sign_in
from fixtures.internal_case_note import internal_case_note
from fixtures.urls import exporter_url, api_url

from pages.add_goods_page import AddGoodPage
from pages.add_new_external_location_form_page import AddNewExternalLocationFormPage
from pages.application_overview_page import ApplicationOverviewPage
from pages.apply_for_a_licence_page import ApplyForALicencePage
from pages.attach_document_page import AttachDocumentPage
from pages.exporter_hub_page import ExporterHubPage
from pages.external_locations_page import ExternalLocationsPage
from pages.preexisting_locations_page import PreexistingLocationsPage
from pages.shared import Shared
from pages.sites_page import SitesPage
from pages.which_location_form_page import WhichLocationFormPage
from pytest_bdd import given, when, then, parsers
import helpers.helpers as utils

# from core import strings

strict_gherkin = False


def pytest_addoption(parser):
    env = str(os.environ.get('ENVIRONMENT'))
    if env == 'None':
        env = "dev"
    parser.addoption("--driver", action="store", default="chrome", help="Type in browser type")
    if env == 'local':
        parser.addoption("--exporter_url", action="store", default="http://localhost:9000", help="url")
        parser.addoption("--lite_api_url", action="store", default="http://localhost:8100", help="url")
    else:
        parser.addoption("--exporter_url", action="store", default="https://exporter.lite.service." + env + ".uktrade.io/", help="url")
        parser.addoption("--lite_api_url", action="store", default="https://lite-api-" + env + ".london.cloudapps.digital/", help="url")
    parser.addoption("--sso_sign_in_url", action="store", default="https://sso.trade.uat.uktrade.io/login/", help="url")
    parser.addoption("--sso-url", action="store", default="https://sso.trade.uat.uktrade.io/login/", help="url")
    parser.addoption("--email", action="store", default="test@mail.com")
    parser.addoption("--password", action="store", default="password")
    parser.addoption("--first_name", action="store", default="Test")
    parser.addoption("--last_name", action="store", default="User")
    # Load in content strings
    # with open('../../lite-content/lite-exporter-frontend/strings.json') as json_file:
    #     strings.constants = json.load(json_file)


def pytest_exception_interact(node, report):
    if node and report.failed:
        class_name = node._nodeid.replace(".py::", "_class_")
        name = "{0}_{1}".format(class_name, "error")
        print(name)
        utils.save_screenshot(node.funcargs.get("driver"), name)


@pytest.fixture(scope="module")
def email(request):
    return request.config.getoption("--email")


@pytest.fixture(scope="module")
def password(request):
    return request.config.getoption("--password")


@pytest.fixture(scope="module")
def first_name(request):
    return request.config.getoption("--first_name")


@pytest.fixture(scope="module")
def last_name(request):
    return request.config.getoption("--last_name")


@given('I go to exporter homepage')
def go_to_exporter(driver, sso_sign_in, exporter_url, register_organisation):
    driver.get(exporter_url)


@when('I go to exporter homepage')
def go_to_exporter_when(driver, exporter_url):
    driver.get(exporter_url)

# utils
@then(parsers.parse('driver title equals "{expected_text}"'))
def assert_title_text(driver, expected_text):
    assert driver.title == expected_text


# applying for licence


@when('I click on apply for a license button')
def click_apply_licence(driver):
    exporter = ExporterHubPage(driver)
    exporter.click_apply_for_a_licence()


@when('I click on start button')
def click_start_button(driver):
    apply = ApplyForALicencePage(driver)
    apply.click_start_now_btn()


@when('I enter in name for application and continue')
def enter_application_name(driver, context):
    apply = ApplyForALicencePage(driver)
    app_time_id = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    context.app_time_id = app_time_id
    app_name = "Request for Nimbus 2000 " + app_time_id
    apply.enter_name_or_reference_for_application(app_name)
    context.app_id = app_name
    apply.click_save_and_continue()


@when(parsers.parse('I select "{type}" application and continue'))
def enter_type_of_application(driver, type, context):
    context.type = type
    # type needs to be standard or open
    apply = ApplyForALicencePage(driver)
    apply.click_export_licence(type)
    apply.click_continue()


@when(parsers.parse('I select "{permanent_or_temporary}" option and continue'))
def enter_permanent_or_temporary(driver, permanent_or_temporary, context):
    context.perm_or_temp = permanent_or_temporary
    # type needs to be permanent or temporary
    apply = ApplyForALicencePage(driver)
    apply.click_permanent_or_temporary_button(permanent_or_temporary)
    apply.click_continue()


@when(parsers.parse('I select "{yes_or_no}" for whether I have an export licence and "{reference}" if I have a reference and continue'))
def enter_export_licence(driver, yes_or_no, reference, context):
    apply = ApplyForALicencePage(driver)
    apply.click_export_licence_yes_or_no(yes_or_no)
    context.ref = reference
    apply.type_into_reference_number(reference)
    apply.click_continue()


@when('I click on application locations link')
def i_click_application_locations_link(driver):
    app = ApplicationOverviewPage(driver)
    app.click_application_locations_link()


@when(parsers.parse('I select "{organisation_or_external}" for where my goods are located'))
def choose_location_type(driver, organisation_or_external):
    which_location_form = WhichLocationFormPage(driver)
    which_location_form.click_on_organisation_or_external_radio_button(organisation_or_external)
    which_location_form.click_continue()


@when(parsers.parse('I fill in new external location form with name: "{name}", address: "{address}" and country: "{country}" and continue'))
def add_new_external_location(driver, name, address, country):
    add_new_external_location_form_page = AddNewExternalLocationFormPage(driver)
    add_new_external_location_form_page.enter_external_location_name(name)
    add_new_external_location_form_page.enter_external_location_address(address)
    add_new_external_location_form_page.enter_external_location_country(country)
    add_new_external_location_form_page.click_continue()


@when(parsers.parse('I select the location at position "{position_number}" in external locations list and continue'))
def assert_checkbox_at_position(driver, position_number):
    preexisting_locations_page = PreexistingLocationsPage(driver)
    preexisting_locations_page.click_external_locations_checkbox(int(position_number)-1)
    preexisting_locations_page.click_continue()


@then(parsers.parse('I see "{number_of_locations}" locations'))
def i_see_a_number_of_locations(driver, number_of_locations):
    assert len(driver.find_elements_by_css_selector('.lite-card')) == int(number_of_locations)


@when('I click on add new address')
def i_click_on_add_new_address(driver):
    external_locations_page = ExternalLocationsPage(driver)
    external_locations_page.click_add_new_address()


@when('I click on preexisting locations')
def i_click_add_preexisting_locations(driver):
    external_locations_page = ExternalLocationsPage(driver)
    external_locations_page.click_preexisting_locations()


@when('I click continue')
def i_click_continue(driver):
    driver.find_element_by_css_selector("button[type*='submit']").click()


@then(parsers.parse('error message is "{expected_error}"'))
def error_message_is(driver, expected_error):
    shared = Shared(driver)
    assert shared.is_error_message_displayed()
    assert expected_error in shared.get_text_of_error_message()


@when(parsers.parse('I select the site at position "{no}"'))
def select_the_site_at_position(driver, no):
    sites = SitesPage(driver)
    sites.click_sites_checkbox(int(no)-1)


@when('I click on applications')
def click_my_application_link(driver):
    exporter_hub = ExporterHubPage(driver)
    exporter_hub.click_applications()


@when('I click on goods link')
def click_my_goods_link(driver):
    exporter_hub = ExporterHubPage(driver)
    exporter_hub.click_my_goods()


@when('I click on goods tile')
def click_my_goods_link(driver):
    exporter_hub = ExporterHubPage(driver)
    driver.execute_script("document.getElementById('goods').scrollIntoView(true);")
    exporter_hub.click_my_goods()


@when('I click on my registered sites')
def click_my_registered_sites(driver):
    which_location = WhichLocationFormPage(driver)
    shared = Shared(driver)
    which_location.click_on_my_sites_radio_button()
    shared.click_continue()


@when('I click on external locations')
def click_external_locations(driver):
    which_location = WhichLocationFormPage(driver)
    shared = Shared(driver)
    which_location.click_on_external_location_radio_button()
    shared.click_continue()


@when('I click the add from organisations goods button')
def click_add_from_organisation_button(driver):
    driver.find_element_by_css_selector('a[href*="add-preexisting"]').click()


@when('I click add a good button')
def click_add_from_organisation_button(driver):
    add_goods_page = AddGoodPage(driver)
    add_goods_page.click_add_a_good()


@when(parsers.parse('I add a good or good type with description "{description}" controlled "{controlled}" control code "{control_code}" incorporated "{incorporated}" and part number "{part}"'))
def add_new_good(driver, description, controlled, control_code, incorporated, part, context):
    good_part_needed = True
    exporter_hub = ExporterHubPage(driver)
    add_goods_page = AddGoodPage(driver)
    date_time = utils.get_current_date_time_string()
    good_description = "%s %s" % (description, date_time)
    good_part = "%s %s" % (part, date_time)
    context.good_description = good_description
    context.part = good_part
    context.control_code = control_code
    add_goods_page.enter_description_of_goods(good_description)
    add_goods_page.select_is_your_good_controlled(controlled)
    add_goods_page.select_is_your_good_intended_to_be_incorporated_into_an_end_product(incorporated)
    if "not needed" in good_part:
        good_part_needed = False
    elif "empty" not in good_part:
        add_goods_page.enter_part_number(good_part)
    if controlled.lower() == 'unsure':
        exporter_hub.click_save_and_continue()
    else:
        add_goods_page.enter_control_code(control_code)
        exporter_hub.click_save_and_continue()
    if good_part_needed:
        context.good_id_from_url = driver.current_url.split('/goods/')[1].split('/')[0]


@when(parsers.parse('I upload file "{filename}" with description "{description}"'))
def upload_a_file(driver, filename, description):
    attach_document_page = AttachDocumentPage(driver)

    # Path gymnastics to get the absolute path for $PWD/../resources/(file_to_upload_x) that works everywhere
    file_to_upload_abs_path = \
        os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'resources', filename))
    if 'ui_automation_tests' not in file_to_upload_abs_path:
        file_to_upload_abs_path = \
            os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'ui_automation_tests/resources', filename))

    attach_document_page.choose_file(file_to_upload_abs_path)
    attach_document_page.enter_description(description)
    attach_document_page.click_submit_btn()


@when(parsers.parse('I raise a clc query control code "{control_code}" description "{description}"'))
def raise_clc_query(driver, control_code, description):
    raise_clc_query_page = AddGoodPage(driver)
    raise_clc_query_page.enter_control_code_unsure(control_code)
    raise_clc_query_page.enter_control_unsure_details(description)
    exporter_hub = ExporterHubPage(driver)
    exporter_hub.click_save_and_continue()
