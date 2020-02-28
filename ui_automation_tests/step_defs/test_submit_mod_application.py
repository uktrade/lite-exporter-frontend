from pytest_bdd import scenarios, when, parsers

from pages.add_end_user_pages import AddEndUserPages
from pages.exporter_hub_page import ExporterHubPage
from pages.shared import Shared
from ui_automation_tests.pages.apply_for_a_licence_page import ApplyForALicencePage
from ui_automation_tests.shared import functions
import ui_automation_tests.shared.tools.helpers as utils

scenarios("../features/submit_mod_application.feature", strict_gherkin=False)


@when(parsers.parse('I select a MOD licence of type "{type}"'))  # noqa
def create_mod_application(driver, context, type):  # noqa
    ApplyForALicencePage(driver).select_mod_application_type(type)
    functions.click_submit(driver)


@when(parsers.parse('I select a licence of type "{type}"'))  # noqa
def create_mod_application(driver, context, type):  # noqa
    ExporterHubPage(driver).click_apply_for_a_licence()
    ApplyForALicencePage(driver).select_licence_type(type)
    functions.click_submit(driver)


@when(  # noqa
    parsers.parse(
        'I add an end user with clearance of sub_type: "{type}", name: "{name}", '
        'website: "{website}", clearance: "{clearance}", address: "{address}" and country "{'
        'country}"'
    )
)
def add_new_end_user_with_clearance(driver, type, name, website, clearance, address, country, context):  # noqa
    add_end_user_pages = AddEndUserPages(driver)
    add_end_user_pages.create_new_or_copy_existing(copy_existing=False)
    add_end_user_pages.select_type(type)
    context.type_end_user = type
    functions.click_submit(driver)
    add_end_user_pages.enter_name(name)
    context.name_end_user = name
    functions.click_submit(driver)
    add_end_user_pages.enter_website(website)
    functions.click_submit(driver)
    no = utils.get_element_index_by_text(Shared(driver).get_radio_buttons_elements(), clearance)
    Shared(driver).click_on_radio_buttons(no)
    functions.click_submit(driver)
    functions.click_submit(driver)
    add_end_user_pages.enter_address(address)
    context.address_end_user = address
    add_end_user_pages.enter_country(country)
    functions.click_submit(driver)
