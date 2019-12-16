import datetime

from pytest_bdd import scenarios, when, then
from selenium.webdriver.common.by import By

import shared.tools.helpers as utils
from pages.add_member import AddMemberPage
from pages.exporter_hub_page import ExporterHubPage
from pages.member_page import MemberPage
from pages.members_page import MembersPage
from pages.shared import Shared
from shared import functions

scenarios("../features/users.feature", strict_gherkin=False)


@then("I add a user")
def add_user(driver):
    members_page = MembersPage(driver)
    add_member_page = AddMemberPage(driver)
    exists = "testuser_1@mail.com" in Shared(driver).get_text_of_body()
    if not exists:
        # Add multiple users for future steps
        for x in range(3):
            i = str(x + 1)
            members_page.click_add_a_member_button()
            add_member_page.enter_email("testuser_" + i + "@mail.com")
            add_member_page.check_all_sites()
            functions.click_submit(driver)


@when("I add user")
def add_user(driver, context, exporter_info):
    user_id = datetime.datetime.now().strftime("%H%M%S")
    first_name = "Test"
    last_name = "User" + user_id
    email_first_part = first_name + last_name
    email = email_first_part.lower() + "@mail.com"
    context.email_to_search = email
    # logged in exporter hub as exporter
    exporter_hub = ExporterHubPage(driver)

    # I want to add a user # I should have an option to manage users
    exporter_hub.click_users()
    elements = driver.find_elements_by_css_selector(".govuk-table__row")
    # When I choose the option to manage users # Then I should see the current user for my company
    no = utils.get_element_index_by_text(elements, exporter_info["email"])
    assert "Active" in elements[no].text

    # And I should have the ability to add a new user
    MembersPage(driver).click_add_a_member_button()
    add_members_page = AddMemberPage(driver)
    add_members_page.enter_email(email)
    add_members_page.check_all_sites()

    # When I Save
    functions.click_submit(driver)


@when("I add self")
def add_self(driver, exporter_info):
    ExporterHubPage(driver).click_users()
    MembersPage(driver).click_add_a_member_button()
    add_members_page = AddMemberPage(driver)
    add_members_page.enter_email(exporter_info["email"])
    add_members_page.check_all_sites()
    functions.click_submit(driver)


@then("user is added")
def user_is_added(driver, context):
    # Then I return to "Manage users" # And I can see the original list of users
    elements = driver.find_elements_by_css_selector(".govuk-table__row")
    no = utils.get_element_index_by_text(elements, context.email_to_search)
    assert "Active" in elements[no].text


@when("I edit user then user is edited")
def user_is_edited(driver, exporter_url, context, exporter_info):
    user_id = datetime.datetime.now().strftime("%d%m%H%M")
    exporter_hub = ExporterHubPage(driver)

    email = context.email_to_search

    email_edited = "testuser_2_edited" + user_id + "@mail.com"
    # Given I am a logged-in user # I want to deactivate users # When I choose the option to manage users
    exporter_hub.click_users()

    # I should have the option to deactivate an active user # edit link, and link from user name
    elements = Shared(driver).get_table_rows()
    no = utils.get_element_index_by_text(Shared(driver).get_table_rows(), email, complete_match=False)
    elements[no].find_element_by_link_text("Edit").click()

    AddMemberPage(driver).enter_email(email_edited)

    functions.click_submit(driver)

    assert utils.is_element_present(driver, By.XPATH, "//*[text()[contains(.,'Test_edited user_2_edited')]]")
    assert utils.is_element_present(driver, By.XPATH, "//*[text()[contains(.,'Test_edited')]]")
    assert utils.is_element_present(driver, By.XPATH, "//*[text()[contains(.,'user_2_edited')]]")
    assert utils.is_element_present(driver, By.XPATH, "//*[text()[contains(.,'" + email_edited + "')]]")

    exporter_hub.go_to(exporter_url)
    exporter_hub.click_users()

    assert utils.is_element_present(driver, By.XPATH, "//*[text()[contains(.,'Test_edited user_2_edited')]]")
    assert utils.is_element_present(driver, By.XPATH, "//*[text()[contains(.,'" + email_edited + "')]]")


@when("I deactivate user then user is deactivated")
def user_is_deactivated(driver, exporter_url, context, request):
    MembersPage(driver).click_view_user_link(context.email_to_search)
    MemberPage(driver).click_deactivate_button()
    assert "Deactivated" in Shared(driver).get_text_of_body(), "user status was expected to be Deactivated"


@when("I reactivate user then user is reactivated")
def user_reactivate(driver, exporter_url, context):
    MemberPage(driver).click_reactivate_button()
    assert "Active" in Shared(driver).get_text_of_body(), "user status was expected to be Deactivated"


@when("I try to deactivate myself I cannot")
def cant_deactivate_self(driver, context):
    exporter_hub = ExporterHubPage(driver)
    exporter_hub.click_user_profile()
    driver.set_timeout_to(0)
    deactivate = utils.is_element_present(driver, By.XPATH, "//*[text()[contains(.,'Deactivate')]]")
    assert not deactivate
    driver.set_timeout_to(10)
