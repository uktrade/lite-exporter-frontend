from faker import Faker
from pytest_bdd import scenarios, when, then, parsers
from selenium.webdriver.support.select import Select

from ui_automation_tests.pages.add_member import AddMemberPage
from ui_automation_tests.pages.member_page import MemberPage
from ui_automation_tests.pages.members_page import MembersPage
from ui_automation_tests.pages.shared import Shared
from ui_automation_tests.shared import functions
from ui_automation_tests.shared.tools.helpers import paginated_item_exists, highlight, get_text_of_multi_page_table
from ui_automation_tests.shared.tools.helpers import scroll_to_element_by_id

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
    scroll_to_element_by_id(driver, "button-Save")
    driver.find_element_by_id("button-Save").click()


@when("I select the member that was just added")
def select_the_member_that_was_just_added(driver, context):
    MembersPage(driver).click_view_member_link(context.email_to_search)


@when("I deactivate them")
def user_deactivate(driver):
    MemberPage(driver).click_deactivate_button()


@then("the member is deactivated")
def user_deactivate(driver):
    # TODO get rid of this body.
    assert "Deactivated" in Shared(driver).get_text_of_body(), "user status was expected to be Deactivated"


@when("I reactivate them")
def user_reactivate(driver):
    MemberPage(driver).click_reactivate_button()


@then("the member is reactivated")
def user_reactivate(driver):
    assert "Active" in Shared(driver).get_text_of_body(), "user status was expected to be Deactivated"


@when("I change what sites they're assigned to")
def change_members_role(driver, context, api_test_client):
    site = api_test_client.organisations.add_site(context.org_id)

    MemberPage(driver).click_assign_sites_button()

    site_checkbox = driver.find_element_by_id(site["name"])
    scroll_to_element_by_id(driver, site["name"])
    site_checkbox.click()
    functions.click_submit(driver)

    assert site["name"] in Shared(driver).get_text_of_body(), "user was expected to be assigned to site"


@when("I change their role to Super User")
def change_members_role(driver):
    MemberPage(driver).click_change_role_button()

    role_select = Select(driver.find_element_by_id("role"))
    role_select.select_by_visible_text("Super User")
    functions.click_submit(driver)


@then("role is changed")
def change_members_role(driver):
    assert "Super User" in Shared(driver).get_text_of_body(), "user role was expected to be Super User"


@when("I show filters")
def show_filters(driver):
    Shared(driver).click_show_filters_link()


@when(parsers.parse('filter status has been changed to "{status}"'))  # noqa
def filter_status_change(driver, status):
    members_page = MembersPage(driver)
    members_page.select_filter_status_from_dropdown(status)
    Shared(driver).click_apply_filters_button()


@then("I see the new member")
def see_new_user(driver, context):
    assert paginated_item_exists(context.email_to_search, driver), "Item couldn't be found"


@then("I do not see the new member")
def do_not_see_new_user(driver, context):
    text = get_text_of_multi_page_table(".govuk-table", driver)
    assert context.email_to_search not in text


@when("I go back to the members page")
def i_go_back_to_the_members_page(driver):
    driver.find_element_by_css_selector("a[href='/organisation/members/']").click()
