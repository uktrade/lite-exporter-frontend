import datetime
from pytest_bdd import scenarios, given, when, then, parsers, scenarios
from pages.apply_for_a_licence_page import ApplyForALicencePage
from pages.exporter_hub_page import ExporterHubPage
from pages.sites_page import SitesPage
from pages.shared import Shared
from conftest import context

scenarios('../features/submit_application.feature')

import logging
log = logging.getLogger()
console = logging.StreamHandler()
log.addHandler(console)


@when('I click on apply for a license button')
def click_apply_licence(driver):
    exporter = ExporterHubPage(driver)
    exporter.click_apply_for_a_licence()


@then('I see the application overview')
def i_see_the_application_overview(driver):
    time_date_submitted = datetime.datetime.now().strftime("%I:%M%p").lstrip("0").replace(" 0", " ").lower() + datetime.datetime.now().strftime(" %d %B %Y")
    apply = ApplyForALicencePage(driver)
    assert apply.get_text_of_application_headers(0) == "Licence Type"
    assert apply.get_text_of_application_headers(1) == "Export Type"
    assert apply.get_text_of_application_headers(2) == "Reference Number"
    assert apply.get_text_of_application_headers(3) == "Created at"
    assert apply.get_text_of_application_results(0) == context.type+"_licence"
    assert apply.get_text_of_application_results(1) == context.perm_or_temp
    assert apply.get_text_of_application_results(2) == context.ref
    # assert apply_for_licence.get_text_of_application_results(3) == datetime.datetime.now().strftime("%b %d %Y, %H:%M%p")
    assert time_date_submitted in apply.get_text_of_application_results(3), "Created date is incorrect on draft overview"
    app_id = driver.current_url[-36:]
    context.app_id = app_id

@when('I click drafts')
def i_click_drafts(driver):
    exporter = ExporterHubPage(driver)
    exporter.click_drafts()

@when('I click the application')
def i_click_the_application(driver):
    drafts_table = driver.find_element_by_class_name("lite-table")
    drafts_table.find_element_by_xpath(".//td/a[contains(@href,'" + context.app_id + "')]").click()
    assert "Overview" in driver.title
    appName = driver.find_element_by_css_selector(".lite-persistent-notice .govuk-link").text
    assert "Test Application" in appName

@when('I delete the application')
def i_delete_the_application(driver):
    apply = ApplyForALicencePage(driver)
    apply.click_delete_application()
    assert 'Exporter Hub - LITE' in driver.title,\
        "failed to go to Exporter Hub page after deleting application from application overview page"

@when('I submit the application')
def submit_the_application(driver):
    apply = ApplyForALicencePage(driver)
    apply.click_submit_application()
    assert apply.get_text_of_success_message() == "Application submitted"


@then('I see no sites attached error message')
def i_see_no_sites_attached_error(driver):
    shared = Shared(driver)
    assert "Cannot create an application with no sites attached" in shared.get_text_of_error_message_at_position_2()


@when('I select the site at position')
def select_the_site_at_position(driver):
    sites = SitesPage(driver)
    apply = ApplyForALicencePage(driver)
    sites.click_sites_checkbox()
    apply.click_save_and_continue()

