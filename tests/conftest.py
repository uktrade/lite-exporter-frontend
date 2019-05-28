import pytest
from selenium import webdriver
from pytest_bdd import scenarios, given, when, then, parsers
from pages.exporter_hub_page import ExporterHubPage
import helpers.helpers as utils
import os

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
@pytest.fixture(scope="module", autouse=True)
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

def test_teardown(driver):
    driver.quit()

@given('I go to internal homepage')
def go_to_internal_homepage(driver, internal_url, internal_login_url):
    driver.get(internal_login_url)
    driver.find_element_by_name("username").send_keys("test-uat-user@digital.trade.gov.uk")
    driver.find_element_by_name("password").send_keys("5cCIlffSrqszgOuw23VEOECnM")
    driver.find_element_by_css_selector("[type='submit']").click()
    driver.get(internal_url)

@given('I login to exporter homepage')
def login_to_exporter(driver, exporter_url):
    exporter_hub = ExporterHubPage(driver)
    driver.get(exporter_url)
    if "login" in driver.current_url:
        exporter_hub.login("test@mail.com", "password")
