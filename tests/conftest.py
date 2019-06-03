import pytest
from selenium import webdriver
from pages.application_overview_page import ApplicationOverviewPage
import os
import datetime
from pytest_bdd import scenarios, given, when, then, parsers, scenarios
from pages.exporter_hub_page import ExporterHubPage

from pages.apply_for_a_licence_page import ApplyForALicencePage
strict_gherkin = False

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
    print("touched: " + env)
    parser.addoption("--driver", action="store", default="chrome", help="Type in browser type")
    #parser.addoption("--exporter_url", action="store", default="https://lite-exporter-frontend-" + env + ".london.cloudapps.digital/", help="url")
    parser.addoption("--exporter_url", action="store", default="localhost:9000/", help="url")
    #parser.addoption("--internal_url", action="store", default="https://lite-internal-frontend-" + env + ".london.cloudapps.digital/", help="url")
    parser.addoption("--internal_url", action="store", default="localhost:8080/", help="url")


# Create driver fixture that initiates chrome
@pytest.fixture(scope="session", autouse=True)
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
        print('only chrome is supported at the moment')
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
def internal_login_url():
    return "https://sso.trade.uat.uktrade.io/login/"

@given('I go to internal homepage')
def go_to_internal_homepage(driver, internal_url, internal_login_url):
    driver.get(internal_login_url)
    driver.find_element_by_name("username").send_keys("test-uat-user@digital.trade.gov.uk")
    driver.find_element_by_name("password").send_keys("5cCIlffSrqszgOuw23VEOECnM")
    driver.find_element_by_css_selector("[type='submit']").click()
    driver.get(internal_url)


@given('I go to exporter homepage')
def go_to_exporter(driver, exporter_url):
    driver.get(exporter_url)

@when(parsers.parse('I login to exporter homepage with username "{username}" and "{password}"'))
def login_to_exporter(driver, username, password):
    exporter_hub = ExporterHubPage(driver)
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
def enter_application_name(driver):
    apply = ApplyForALicencePage(driver)
    app_time_id = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    app_name = "Test Application " + app_time_id
    apply.enter_name_or_reference_for_application(app_name)
    context.app_id = app_name
    apply.click_save_and_continue()


@when(parsers.parse('I select "{type}" application and continue'))
def enter_type_of_application(driver, type):
    context.type = type
    # type needs to be standard or temporary
    apply = ApplyForALicencePage(driver)
    apply.click_export_licence(type)
    apply.click_continue()


@when(parsers.parse('I select "{permanent_or_temporary}" option and continue'))
def enter_permanent_or_temporary(driver, permanent_or_temporary):
    context.perm_or_temp = permanent_or_temporary
    # type needs to be standard or temporary
    apply = ApplyForALicencePage(driver)
    apply.click_permanent_or_temporary_button(permanent_or_temporary)
    apply.click_continue()

@when(parsers.parse('I select "{yes_or_no}" for whether I have an export licence and "{reference}" if I have a reference and continue'))
def enter_export_licence(driver, yes_or_no, reference):
    apply = ApplyForALicencePage(driver)
    apply.click_export_licence_yes_or_no(yes_or_no)
    context.ref = reference
    apply.type_into_reference_number(reference)
    apply.click_continue()

@when('I click sites link')
def i_click_sites_link(driver):
    app = ApplicationOverviewPage(driver)
    app.click_sites_link()

@when('I click continue')
def i_click_continue(driver):
    driver.find_element_by_css_selector("button[type*='submit']").click()
