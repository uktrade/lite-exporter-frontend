from pytest_bdd import scenarios, then, parsers, when, given
from directory_sso_api_client.client import sso_api_client

scenarios("../features/login_logout.feature", strict_gherkin=False)


@then(parsers.parse('page title equals "{expected_text}"'))
def assert_title_text(driver, expected_text):
    assert driver.title == expected_text


@when("I click the logout link")
def click_the_logout_link(driver):
    driver.find_element_by_link_text("Sign out").click()


@then("I am taken to the GREAT.GOV.UK page")
def taken_to_the_great_page(driver):
    assert "logout" in driver.current_url


@given("I create a new user")
def create_new_user():
    response = sso_api_client.get("/testapi/user-by-email/email_here/")
    print(response)
