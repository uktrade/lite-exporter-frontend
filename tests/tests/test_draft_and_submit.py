from selenium import webdriver
import unittest
import datetime
import os
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from pages.exporter_hub_page import ExporterHubPage
from pages.apply_for_a_licence_page import ApplyForALicencePage
from pages.applications_page import ApplicationsPage
import helpers.helpers as utils
import pytest
import logging
log = logging.getLogger()
console = logging.StreamHandler()
log.addHandler(console)


def test_submit_application(driver, open_exporter_hub, exporter_url):

    exporter_hub.go_to(exporter_url)
    logging.info("n Exporter Hub Page")

    exporter_hub.click_applications()
    logging.info("Clicked Applications")

    assert utils.is_element_present(driver, By.XPATH, "//*[text()[contains(.,'" + app_time_id + "')]]")
    log.info("application found in submitted applications list")

    # Check application status is Submitted
    log.info("verifying application status is Submitted")
    status = driver.find_element_by_xpath("//*[text()[contains(.,'" + app_time_id + "')]]/following-sibling::td[last()]")
    assert status.is_displayed()
    assert status.text == "Submitted", "Expected Status of application is to be 'Submitted' but is not"
    logging.info("Test Complete")


def test_must_enter_fields_for_application(driver, open_exporter_hub):
    logging.info("Test Started")
    exporter_hub = ExporterHubPage(driver)
    apply_for_licence = ApplyForALicencePage(driver)
    if "login" in driver.current_url:
        log.info("logging in as test@mail.com")
        exporter_hub.login("test@mail.com", "password")

    exporter_hub.click_apply_for_a_licence()
    logging.info("Clicked apply for a licence")
    apply_for_licence.click_start_now_btn()
    logging.info("Clicked start button")

    logging.info("no name or reference entered")
    logging.info("clicked save and continue")
    apply_for_licence.click_save_and_continue()

    element = driver.find_element_by_css_selector('.govuk-error-summary')
    assert element.is_displayed()
    assert 'There are errors on this page\nEnter a reference name for your application.' in element.text
    logging.info("Error displayed successfully")

    apply_for_licence.enter_name_or_reference_for_application("a")
    apply_for_licence.click_save_and_continue()

    logging.info("no type of license option entered")
    logging.info("clicked  continue")
    apply_for_licence.click_continue()

    element = driver.find_element_by_css_selector('.govuk-error-summary')
    assert element.is_displayed()
    assert 'There are errors on this page\nSelect which type of licence you want to apply for.' in element.text
    logging.info("Error displayed successfully")

    apply_for_licence.click_export_licence("standard")

    apply_for_licence.click_continue()

    logging.info("no temporary or permanent option selected entered")
    logging.info("clicked  continue")
    apply_for_licence.click_continue()

    element = driver.find_element_by_css_selector('.govuk-error-summary')
    assert element.is_displayed()
    assert 'There are errors on this page\nSelect if you want to apply for a temporary or permanent licence.' in element.text
    logging.info("Error displayed successfully")

    apply_for_licence.click_permanent_or_temporary_button("temporary")
    apply_for_licence.click_continue()

    logging.info("no permission of export license selected")
    logging.info("clicked continue")
    apply_for_licence.click_continue()

    element = driver.find_element_by_css_selector('.govuk-error-summary'), "Expected validation error for Have you " \
                                                                           "been told that you need an export licence " \
                                                                           "by an official? "
    assert element.is_displayed()
    assert 'There are errors on this page\nSelect if you have permission.' in element.text
    logging.info("Error displayed successfully")

    apply_for_licence.click_export_licence_yes_or_no("yes")
    apply_for_licence.click_continue()

    apply_for_licence.click_delete_application()
    assert 'Exporter Hub - LITE' in driver.title, "Delete Application link on overview page failed to go to Exporter Hub page"


def test_status_column_and_refresh_btn_on_applications(driver, open_exporter_hub):
    logging.info("Test Started")
    exporter_hub = ExporterHubPage(driver)
    applications = ApplicationsPage(driver)
    if "login" in driver.current_url:
        log.info("logging in as test@mail.com")
        exporter_hub.login("test@mail.com", "password")

    exporter_hub.click_applications()
    logging.info("navigated to applications page")

    assert driver.find_element_by_xpath("// th[text()[contains(., 'Status')]]").is_displayed()
    logging.info("Status column is displayed")

    applications.click_refresh_btn()
    logging.info("clicked refresh button")

    logging.info("Test Complete")


def test_teardown(driver):
    driver.quit()
