from pytest_bdd import scenarios, then, given

scenarios("../features/register_an_organisation.feature", strict_gherkin=False)


@then("I should see a success page")
def success():
    raise NotImplementedError("STEP: Then I should see a success page")


@given("I am logged in but I don't belong to an organisation")
def new_log_in():
    pass
    # response = sso_api_client.get("/testapi/user-by-email/email_here/")
    # print(response)
    # response = sso_api_client.post("/testapi/test-users/", data={})
    # response = response.json()["email"]
