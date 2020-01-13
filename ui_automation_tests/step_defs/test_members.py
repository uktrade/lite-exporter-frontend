from faker import Faker
from pytest_bdd import scenarios, when, then
from selenium.webdriver.support.select import Select

from pages.add_member import AddMemberPage
from pages.exporter_hub_page import ExporterHubPage
from pages.member_page import MemberPage
from pages.members_page import MembersPage
from pages.shared import Shared
from shared import functions
from shared.api.organisations import add_site
from shared.tools.helpers import scroll_to_element_by_id

scenarios("../features/members.feature", strict_gherkin=False)

fake = Faker()


@when("I add a member to the organisation")
def add_member(driver, context):
    members_page = MembersPage(driver)
    add_member_page = AddMemberPage(driver)
    members_page.click_add_a_member_button()

    email = fake.email()
    context.email_to_search = email
    add_member_page.enter_email(email)

    add_member_page.check_all_sites()
    functions.click_submit(driver)


@when("I select the member that was just added")
def select_the_member_that_was_just_added(driver, context):
    MembersPage(driver).click_view_member_link(context.email_to_search)


@when("I deactivate them, then the member is deactivated")
def user_deactivate(driver):
    MemberPage(driver).click_deactivate_button()
    assert "Deactivated" in Shared(driver).get_text_of_body(), "user status was expected to be Deactivated"


@when("I reactivate them, then the member is reactivated")
def user_reactivate(driver):
    MemberPage(driver).click_reactivate_button()
    assert "Active" in Shared(driver).get_text_of_body(), "user status was expected to be Deactivated"


@when("I change what sites they're assigned to")
def change_members_role(driver, context, user_details):
    site = add_site(context.org_id, context.exporter_headers)

    MemberPage(driver).click_assign_sites_button()

    site_checkbox = driver.find_element_by_id(site["name"])
    scroll_to_element_by_id(driver, site["name"])
    site_checkbox.click()
    functions.click_submit(driver)

    assert site["name"] in Shared(driver).get_text_of_body(), "user was expected to be assigned to site"


@then("I change their role")
def change_members_role(driver):
    MemberPage(driver).click_change_role_button()

    role_select = Select(driver.find_element_by_id("role"))
    role_select.select_by_visible_text("Super User")
    functions.click_submit(driver)

    assert "Super User" in Shared(driver).get_text_of_body(), "user role was expected to be Super User"


@when("I try to deactivate myself I cannot")
def cant_deactivate_self(driver, context):
    exporter_hub = ExporterHubPage(driver)
    exporter_hub.click_user_profile()

    member_page = MemberPage(driver)
    member_page.try_click_more_actions_button()
    assert not functions.element_with_id_exists(driver, member_page.BUTTON_DEACTIVATE_ID)
