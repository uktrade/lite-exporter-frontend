from pytest_bdd import when, then, scenarios, given

from helpers import helpers
from pages.exporter_hub_page import ExporterHubPage
from pages.hmrc_query_page import HMRCQueryPage
from pages.hub_page import Hub
from pages.shared import Shared

scenarios('../features/hmrc.feature', strict_gherkin=False)


@given("I have a second set up organisation")
def set_up_second_organisation(register_organisation_for_switching_organisation):
    pass


@when("I switch organisations to my second organisation")
def switch_organisations_to_my_second_organisation(driver, context):
    Hub(driver).click_switch_link()
    no = helpers.get_element_index_by_text(Shared(driver).get_radio_buttons_elements(), context.org_name_for_switching_organisations)
    Shared(driver).click_on_radio_buttons(no)
    Shared(driver).click_continue()


@when("I select to raise a query for my first organisation")
def raise_query_on_behlaf_of_my_first_org(driver, context):
    ExporterHubPage(driver).click_raise_hmrc_query()
    page = HMRCQueryPage(driver)
    page.search_for_org(context.org_name)
    Shared(driver).click_continue()
    page.select_first_org()
