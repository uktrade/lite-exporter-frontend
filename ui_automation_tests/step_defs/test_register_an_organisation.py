from pytest_bdd import scenarios, then, given, when

from shared.api_client.sub_helpers.users import post_user_to_great_sso

scenarios("../features/register_an_organisation.feature", strict_gherkin=False)


@then("I should see a success page")
def success():
    raise NotImplementedError("STEP: Then I should see a success page")


@given("I register but I don't belong to an organisation")
def new_log_in(context):
    response = post_user_to_great_sso()
    context.newly_registered_email = response["email"],
    context.newly_registered_password = response["password"],


@when("I click the register button")
def register():
    pass
