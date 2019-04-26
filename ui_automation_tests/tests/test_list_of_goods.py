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


@pytest.fixture(scope="function")
def open_exporter_hub(driver, url):
    # navigate to the application home page
    driver.get(url)
    # driver.maximize_window()


def test_add_goods_to_list_of_goods(driver, open_exporter_hub, url):
    exporter_hub = ExporterHubPage(driver)
    exporter_hub.login("test@mail.com", "password")

    time_id = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Click My goods assert is on the my goods page
    exporter_hub.click_my_goods()
    exporter_hub.click_add_a_good()

    # Add good details
    exporter_hub.enter_description_of_goods("This is a description of good " + time_id)
    exporter_hub.select_is_your_good_controlled("Yes")
    exporter_hub.enter_control_code("ML6")
    exporter_hub.select_is_your_good_intended_to_be_incorporated_into_an_end_product("Yes")
    exporter_hub.enter_part_number("part-123")
    exporter_hub.click_save_and_continue()

    # Assert good is added to the goods list on the goods page
    exporter_hub.verify_good_is_in_goods_list(time_id, "part-123", "ML6")

    logging.info("Test Complete")


def test_teardown(driver):
    driver.quit()
