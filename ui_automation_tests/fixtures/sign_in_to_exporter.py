from pytest import fixture
from pages.exporter_hub_page import ExporterHubPage


@fixture(scope="function")
def sign_in_to_exporter(driver, request, exporter_sso_login_info):
    driver.get(request.config.getoption("--exporter_url"))
    exporter_hub = ExporterHubPage(driver)
    if "login" in driver.current_url:
        exporter_hub.login(exporter_sso_login_info['email'], exporter_sso_login_info['password'])
