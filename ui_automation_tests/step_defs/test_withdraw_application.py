from pytest_bdd import scenarios, then

scenarios('../features/withdraw_application.feature')


@then("I click the button 'Withdraw Application'")
def i_click_withdraw_application(driver):
    pass


@then("I should see a confirmation page")
def i_click_withdraw_application(driver):
    pass


@then("I select the yes radiobutton")
def i_click_withdraw_application(driver):
    pass


@then("the application will have a status of “withdrawn”")
def i_click_withdraw_application(driver):
    pass


@then("I won't be able to see the withdraw button")
def i_click_withdraw_application(driver):
    pass
