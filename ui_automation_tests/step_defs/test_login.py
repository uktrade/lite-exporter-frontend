from pytest_bdd import scenarios, then, parsers, when

scenarios('../features/login_logout.feature', strict_gherkin=False)


@then(parsers.parse('page title equals "{expected_text}"'))
def assert_title_text(driver, expected_text):
    assert driver.title == expected_text


@when("I click the logout link")
def step_impl(driver):
    driver.find_element_by_link_text('Sign out').click()


@then("I am taken to the GREAT.GOV.UK page")
def step_impl(driver):
    assert 'logout' in driver.current_url
