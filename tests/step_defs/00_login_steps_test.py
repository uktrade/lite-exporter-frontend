from pytest_bdd import scenarios, given, when, then, parsers
from pages.shared import Shared
scenarios('../features/login_invalid.feature')

@then('I see login error message')
def login_error_message(driver):
    shared = Shared(driver)
    assert "Enter a valid email/password combination" in shared.get_text_of_error_message()
