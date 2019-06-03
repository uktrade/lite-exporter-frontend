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


def test_search_for_goods_by_description(driver, open_exporter_hub):
    exporter_hub = ExporterHubPage(driver)
    apply_for_licence = ApplyForALicencePage(driver)
    goods = ApplyForALicencePage(driver)

    if "login" in driver.current_url:
        log.info("logging in as test@mail.com")
        exporter_hub.login("test@mail.com", "password")

    log.info("Submitting application")
    app_time_id = datetime.datetime.now().strftime("m%d%H%M%S")
    app_name = str("Test Application " + app_time_id)

    exporter_hub.click_apply_for_a_licence()
    apply_for_licence.click_start_now_btn()
    apply_for_licence.enter_application_details_new(name=app_name, licence_type="standard", temp_or_perm="temporary", need_licence="yes", ref_number="123456")
    apply_for_licence.click_save_and_continue()
    app_id = driver.current_url[-46:].replace('/overview/', '')
    log.info("Application submitted")

    assert "Overview" in driver.title

    goods.click_goods_link()
    goods.click_add_from_organisations_goods()

    goods.enter_description("Good T1")
    goods.click_filter_btn()

    goods = driver.find_elements_by_xpath("//div[@class='lite-item']")
    assert len(goods) == 1
    assert goods[0].find_element(By.TAG_NAME, "h4").text == "Good T1"


def test_search_for_goods_by_part_number(driver, open_exporter_hub):
    exporter_hub = ExporterHubPage(driver)
    apply_for_licence = ApplyForALicencePage(driver)
    goods = ApplyForALicencePage(driver)

    if "login" in driver.current_url:
        log.info("logging in as test@mail.com")
        exporter_hub.login("test@mail.com", "password")

    log.info("Submitting application")
    app_time_id = datetime.datetime.now().strftime("m%d%H%M%S")
    app_name = str("Test Application " + app_time_id)

    exporter_hub.click_apply_for_a_licence()
    apply_for_licence.click_start_now_btn()
    apply_for_licence.enter_application_details_new(name=app_name, licence_type="standard", temp_or_perm="temporary", need_licence="yes", ref_number="123456")
    apply_for_licence.click_save_and_continue()
    app_id = driver.current_url[-46:].replace('/overview/', '')
    log.info("Application submitted")

    assert "Overview" in driver.title

    goods.click_goods_link()
    goods.click_add_from_organisations_goods()

    goods.enter_part_number("G1-12")
    goods.click_filter_btn()

    goods = driver.find_elements_by_xpath("//div[@class='lite-item']")
    assert len(goods) == 1
    assert "G1-12" in goods[0].text


def test_remove_filter(driver, open_exporter_hub):
    exporter_hub = ExporterHubPage(driver)
    apply_for_licence = ApplyForALicencePage(driver)
    goods = ApplyForALicencePage(driver)

    if "login" in driver.current_url:
        log.info("logging in as test@mail.com")
        exporter_hub.login("test@mail.com", "password")

    log.info("Submitting application")
    app_time_id = datetime.datetime.now().strftime("m%d%H%M%S")
    app_name = str("Test Application " + app_time_id)

    exporter_hub.click_apply_for_a_licence()
    apply_for_licence.click_start_now_btn()
    apply_for_licence.enter_application_details_new(name=app_name, licence_type="standard", temp_or_perm="temporary", need_licence="yes", ref_number="123456")
    apply_for_licence.click_save_and_continue()
    app_id = driver.current_url[-46:].replace('/overview/', '')
    log.info("Application submitted")

    assert "Overview" in driver.title

    goods.click_goods_link()
    goods.click_add_from_organisations_goods()

    goods.enter_description("Good T1")
    goods.enter_part_number("G1-12")
    goods.click_filter_btn()

    goods = driver.find_elements_by_xpath("//div[@class='lite-item']")
    assert len(goods) == 1

    filter_tags = driver.find_elements_by_css_selector(".lite-filter-bar a")
    for tag in range(len(filter_tags)):
        driver.find_element_by_css_selector(".lite-filter-bar a").click()

    goods = driver.find_elements_by_xpath("//div[@class='lite-item']")
    assert len(goods) > 1


def test_teardown(driver):
    driver.quit()
