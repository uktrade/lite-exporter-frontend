from pytest_bdd import scenarios, given, when

from ui_automation_tests.shared.fixtures.apply_for_application import apply_for_trade_control_application
from ui_automation_tests.pages.f680_additional_information_page import F680AdditionalInformationPage
from ui_automation_tests.shared import functions

scenarios("../features/edit_trade_control_application.feature", strict_gherkin=False)


@given("I create a trade control application via api")  # noqa
def trade_control_application_exists(apply_for_trade_control_application):  # noqa
    pass
