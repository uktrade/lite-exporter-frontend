import urllib.request

from pytest_bdd import scenarios, then, when

scenarios("../features/menu.feature", strict_gherkin=False)


@then("I get a 200")
def success(driver):
    conn = urllib.request.urlopen(driver.current_url)
    assert conn.getcode() == 200
    assert driver.find_element_by_id(
        "link-sign-out"
    ).is_displayed(), "Log out button is displayed. User may have the service unavailable screen."


@when("I refresh the page")
def refresh(driver):
    driver.refresh()
