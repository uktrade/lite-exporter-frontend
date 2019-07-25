import datetime
import json
import os
import random

import pytest

from pages.add_end_user_pages import AddEndUserPages
from pages.add_goods_page import AddGoodPage
from pages.add_new_external_location_form_page import AddNewExternalLocationFormPage
from pages.application_goods_list import ApplicationGoodsList
from pages.application_overview_page import ApplicationOverviewPage
from pages.application_page import ApplicationPage
from pages.apply_for_a_licence_page import ApplyForALicencePage
from selenium.webdriver.common.by import By
from pages.exporter_hub_page import ExporterHubPage
from pages.external_locations_page import ExternalLocationsPage
from pages.preexisting_locations_page import PreexistingLocationsPage
from pages.shared import Shared
from pages.sites_page import SitesPage
from pages.which_location_form_page import WhichLocationFormPage
from pytest_bdd import given, when, then, parsers
from selenium import webdriver
from conf.settings import env
import helpers.helpers as utils
from pages.internal_hub_page import InternalHubPage

# from core import strings

strict_gherkin = False


sso_email = env('TEST_SSO_EMAIL')
sso_password = env('TEST_SSO_PASSWORD')

# Screenshot in case of any test failure
def pytest_exception_interact(node, report):
    if node and report.failed:
        class_name = node._nodeid.replace(".py::", "_class_")
        name = "{0}_{1}".format(class_name, exporter_url)
        # utils.save_screenshot(node.funcargs.get("driver"), name)


# Create driver and url command line addoption
def pytest_addoption(parser):
    env = str(os.environ.get('ENVIRONMENT'))
    if env == 'None':
        env = "dev"
    parser.addoption("--driver", action="store", default="chrome", help="Type in browser type")
    parser.addoption("--exporter_url", action="store", default="https://exporter.lite.service." + env + ".uktrade.io/", help="url")
    parser.addoption("--internal_url", action="store", default="https://internal.lite.service." + env + ".uktrade.io/", help="url")
    # parser.addoption("--exporter_url", action="store", default="http://localhost:9000", help="url")
    # parser.addoption("--internal_url", action="store", default="http://localhost:8080", help="url")
    parser.addoption("--sso-url", action="store", default="https://sso.trade.uat.uktrade.io/login/", help="url")
    parser.addoption("--email", action="store", default="test@mail.com")
    parser.addoption("--password", action="store", default="password")
    parser.addoption("--first_name", action="store", default="Test")
    parser.addoption("--last_name", action="store", default="User")

    # Load in content strings
    # with open('../../lite-content/lite-exporter-frontend/strings.json') as json_file:
    #     strings.constants = json.load(json_file)


# Create driver fixture that initiates chrome
@pytest.fixture(scope="session", autouse=True)
@pytest.mark.order(1)
def driver(request):
    browser = request.config.getoption("--driver")
    if browser == 'chrome':
        if str(os.environ.get('ENVIRONMENT')) == 'None':
            browser = webdriver.Chrome("chromedriver")
        else:
            browser = webdriver.Chrome()
        browser.get("about:blank")
        browser.implicitly_wait(10)
        return browser
    else:
        print('Only Chrome is supported at the moment')

    def fin():
        driver.quit()
        request.addfinalizer(fin)


# Create url fixture
@pytest.fixture(scope="module")
def exporter_url(request):
    return request.config.getoption("--exporter_url")


@pytest.fixture(scope="module")
def internal_url(request):
    return request.config.getoption("--internal_url")


@pytest.fixture(scope="module")
def internal_login_url(request):
    return request.config.getoption("--sso-url")


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


@pytest.fixture(scope="session")
def org_setup(driver, request):
    driver.get(request.config.getoption("--sso-url"))
    driver.find_element_by_name("username").send_keys(sso_email)
    driver.find_element_by_name("password").send_keys(sso_password)
    driver.find_element_by_css_selector("[type='submit']").click()
    driver.get(request.config.getoption("--internal_url"))
    internal_hub = InternalHubPage(driver)

    internal_hub.click_manage_organisations_link()

    exists = utils.is_element_present(driver, By.XPATH, "//*[text()[contains(.,'Test Org')]]")
    if not exists:
        # New Organisation
        internal_hub.click_new_organisation()

        internal_hub.enter_business_name("Test Org")
        internal_hub.enter_eori_number("GB987654312000")
        internal_hub.enter_sic_number("73200")
        internal_hub.enter_vat_number("123456789")
        internal_hub.enter_company_registration_number("000000011")
        internal_hub.click_save_and_continue()

        internal_hub.enter_site_name("Site 1")
        internal_hub.enter_address_line_1("123 Cobalt Street")
        internal_hub.enter_address_line_2("123 Cobalt Street")
        internal_hub.enter_zip_code("N23 6YL")
        internal_hub.enter_city("London")
        internal_hub.enter_state("London")
        internal_hub.enter_country("Ukraine")

        internal_hub.click_save_and_continue()

        internal_hub.enter_email("test@mail.com")
        internal_hub.enter_first_name("Test")
        internal_hub.enter_last_name("User1")
        internal_hub.enter_password("password")

        internal_hub.click_submit()
        exists = utils.is_element_present(driver, By.XPATH, "//*[text()[contains(.,'Test Org')]]")
        assert exists


@given('I go to internal homepage')
def go_to_internal_homepage(driver, internal_url, internal_login_url):
    driver.get(internal_login_url)
    driver.find_element_by_name("username").send_keys(sso_email)
    driver.find_element_by_name("password").send_keys(sso_password)
    driver.find_element_by_css_selector("[type='submit']").click()
    driver.get(internal_url)


@when('I go to internal homepage')
def go_to_internal_homepage(driver, internal_url, internal_login_url):
    driver.get(internal_login_url)
    driver.find_element_by_name("username").send_keys(sso_email)
    driver.find_element_by_name("password").send_keys(sso_password)
    driver.find_element_by_css_selector("[type='submit']").click()
    driver.get(internal_url)


@given('I go to exporter homepage')
def go_to_exporter(driver, exporter_url):
    driver.get(exporter_url)


@when('I go to exporter homepage')
def go_to_exporter_when(driver, exporter_url):
    driver.get(exporter_url)


@when(parsers.parse('I login to exporter homepage with username "{username}" and "{password}"'))
def login_to_exporter(driver, username, password, exporter_url, org_setup):
    exporter_hub = ExporterHubPage(driver)
    driver.get(exporter_url)
    if "login" in driver.current_url:
        exporter_hub.login(username, password)

# utils
@then(parsers.parse('driver title equals "{expected_text}"'))
def assert_title_text(driver, expected_text):
    assert driver.title == expected_text


@pytest.fixture
def context():
    class Context(object):
        pass

    return Context()


@pytest.fixture
def test_teardown(driver):
    driver.quit()


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
    app_name = "Request for Nimbus 2000" + app_time_id
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
    if "empty" not in good_part:
        add_goods_page.enter_part_number(good_part)
    if controlled.lower() == 'unsure':
        add_goods_page.enter_control_code_unsure(control_code)
        add_goods_page.enter_control_unsure_details(description + " unsure")
        exporter_hub.click_save_and_continue()
        add_goods_page.select_control_unsure_confirmation("yes")
    else:
        add_goods_page.enter_control_code(control_code)
    exporter_hub.click_save_and_continue()


@pytest.fixture(scope="module")
def create_note_visible_to_exporter(driver, request, internal_login_url, internal_url, context):
    driver.get(internal_login_url)
    driver.find_element_by_name("username").send_keys(sso_email)
    driver.find_element_by_name("password").send_keys(sso_password)
    driver.find_element_by_css_selector("[type='submit']").click()
    driver.get(internal_url)
    driver.find_element_by_xpath("//*[text()[contains(.,'" + context.app_id + "')]]").click()
    application_page = ApplicationPage(driver)
    text = "I love toast"
    context.text = text
    application_page.enter_case_note(text)
    application_page.click_visible_to_exporter_checkbox()
    application_page.click_post_note_btn()
    alert = driver.switch_to_alert()
    alert.accept()



@pytest.fixture(scope="module")
def set_up_application_before_hook(driver, request, exporter_url, org_setup, context):

    apply = ApplyForALicencePage(driver)
    exporter_hub = ExporterHubPage(driver)
    add_goods_page = AddGoodPage(driver)
    which_location_form = WhichLocationFormPage(driver)
    external_locations_page = ExternalLocationsPage(driver)
    add_new_external_location_form_page = AddNewExternalLocationFormPage(driver)
    preexisting_locations_page = PreexistingLocationsPage(driver)
    overview_page = ApplicationOverviewPage(driver)
    add_end_user_pages = AddEndUserPages(driver)

    username = "test@mail.com"
    password = "password"
    type = "standard"
    permanent_or_temporary = "permanent"
    yes_or_no = "yes"
    reference = "123456"
    organisation_or_external = "external"
    name = "32 Lime Street"
    address = "London"
    country = "Ukraine"

    driver.get(exporter_url)
    if "login" in driver.current_url:
        exporter_hub.login(username, password)
    exporter_hub.click_my_goods()
    add_goods_page.click_add_a_good()

    description = "Chinook"
    controlled = "Yes"
    control_code = "1234"
    incorporated = "Yes"
    part = "321"

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
    if "empty" not in good_part:
        add_goods_page.enter_part_number(good_part)
    if controlled.lower() == 'unsure':
        add_goods_page.enter_control_code_unsure(control_code)
        add_goods_page.enter_control_unsure_details(description + " unsure")
        exporter_hub.click_save_and_continue()
        add_goods_page.select_control_unsure_confirmation("yes")
    else:
        add_goods_page.enter_control_code(control_code)
    exporter_hub.click_save_and_continue()
    driver.get(exporter_url)
    exporter_hub.click_apply_for_a_licence()
    apply.click_start_now_btn()
    app_time_id = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    context.app_time_id = app_time_id
    app_name = "Request for Nimbus 2000" + app_time_id
    apply.enter_name_or_reference_for_application(app_name)
    context.app_id = app_name
    apply.click_save_and_continue()
    context.type = type
    # type needs to be standard or open
    apply = ApplyForALicencePage(driver)
    apply.click_export_licence(type)
    apply.click_continue()
    context.perm_or_temp = permanent_or_temporary
    # type needs to be permanent or temporary
    apply = ApplyForALicencePage(driver)
    apply.click_permanent_or_temporary_button(permanent_or_temporary)
    apply.click_continue()
    apply = ApplyForALicencePage(driver)
    apply.click_export_licence_yes_or_no(yes_or_no)
    context.ref = reference
    apply.type_into_reference_number(reference)
    apply.click_continue()
    overview_page.click_application_locations_link()
    which_location_form.click_on_organisation_or_external_radio_button(organisation_or_external)
    which_location_form.click_continue()
    external_locations_page.click_add_new_address()
    add_new_external_location_form_page.enter_external_location_name(name)
    add_new_external_location_form_page.enter_external_location_address(address)
    add_new_external_location_form_page.enter_external_location_country(country)
    add_new_external_location_form_page.click_continue()
    external_locations_page.click_add_new_address()
    name = "place"
    address = "1 Paris Road"
    country = "Ukraine"
    add_new_external_location_form_page.enter_external_location_name(name)
    add_new_external_location_form_page.enter_external_location_address(address)
    add_new_external_location_form_page.enter_external_location_country(country)
    add_new_external_location_form_page.click_continue()
    external_locations_page.click_preexisting_locations()
    preexisting_locations_page.click_external_locations_checkbox(int("2") - 1)
    preexisting_locations_page.click_continue()
    driver.find_element_by_css_selector("a[href*='overview'").click()
    driver.execute_script("document.getElementById('goods').scrollIntoView(true);")
    overview_page.click_goods_link()
    driver.find_element_by_css_selector('a[href*="add-preexisting"]').click()
    no = 1
    context.goods_name = driver.find_elements_by_css_selector('.lite-card .govuk-heading-s')[int(no) - 1].text
    context.part_number = driver.find_elements_by_css_selector('.lite-card .govuk-label')[int(no) - 1].text
    driver.find_elements_by_css_selector('a.govuk-button')[int(no) - 1].click()
    quantity = "1"
    value = "123"
    unit = "Metre"
    context.quantity = quantity
    context.value = value
    context.unit = unit
    application_goods_list = ApplicationGoodsList(driver)
    application_goods_list.add_values_to_good(str(value), str(quantity), unit)
    driver.find_element_by_css_selector("button[type*='submit']").click()
    application_goods_list.click_on_overview()
    overview_page.click_end_user_link()
    type = "government"
    name = "Mr Smith"
    website = "https://www.smith.com"
    address = "London"
    add_end_user_pages.select_type(type)
    context.type_end_user = type
    add_end_user_pages.click_continue()
    add_end_user_pages.enter_name(name)
    context.name_end_user = name
    add_end_user_pages.click_continue()
    add_end_user_pages.enter_website(website)
    add_end_user_pages.click_continue()
    add_end_user_pages.enter_address(address)
    context.address_end_user = address
    add_end_user_pages.enter_country(country)
    add_end_user_pages.click_continue()
    apply.click_submit_application()
    url = driver.current_url.replace('/overview/', '')
    context.app_id = url[-36:]
