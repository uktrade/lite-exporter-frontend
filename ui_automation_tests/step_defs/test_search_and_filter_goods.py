from urllib.parse import urlencode

from pytest_bdd import when, then, parsers, scenarios
from pages.application_goods_list import ApplicationGoodsList
from shared.tools.utils import get_lite_client
from shared.seed_data.request_data import create_good

scenarios("../features/search_and_filter_goods.feature", strict_gherkin=False)


@when(parsers.parse('I filter by part number "{part_number}" and click filter'))
def filter_by_part_no(driver, context, part_number):
    application_goods_list = ApplicationGoodsList(driver)
    application_goods_list.type_into_filter_part_number_search_box_and_filter(part_number)


@when(parsers.parse('I filter by description "{description}" and click filter'))
def filter_by_description(driver, context, description):
    application_goods_list = ApplicationGoodsList(driver)
    application_goods_list.type_into_filter_description_search_box_and_filter(description)


@when(parsers.parse('I filter by control list entry "{control_list}" and click filter'))
def filter_by_description(driver, context, control_list):
    application_goods_list = ApplicationGoodsList(driver)
    application_goods_list.type_into_filter_control_rating_search_box_and_filter(control_list)


@then("I see all goods")
def see_all_goods(driver, context):
    goods_list = ApplicationGoodsList(driver).get_good_descriptions()
    assert len(goods_list) == context.total_goods


@when(
    parsers.parse(
        'I create a good of description "{description}", control code "{control_code}" and part number "{part_number}" if it does not exist'
    )
)
def add_a_good(context, description, control_code, part_number, seed_data_config):
    lite_client = get_lite_client(context, seed_data_config=seed_data_config)
    params = {"description": description, "control_rating": control_code, "part_number": part_number}
    goods = lite_client.seed_good.get_goods(urlencode(params))
    if not len(goods):
        good = create_good(
            description=description, is_end_product=True, control_code=control_code, part_number=part_number
        )
        lite_client.seed_good.add_good(good)
    context.total_goods = len(lite_client.seed_good.get_goods())  # gets count of paginated page


@then(parsers.parse('All goods have description "{description}"'))
def good_description_is_found(driver, description):
    goods_list = ApplicationGoodsList(driver).get_good_descriptions()
    assert len(goods_list) > 0
    for good in goods_list:
        assert good.text == description


@then(parsers.parse('All goods have part number "{part_number}"'))
def good_part_number_is_found(driver, part_number):
    goods_list = ApplicationGoodsList(driver).get_good_part_numbers()
    assert len(goods_list) > 0
    for good in goods_list:
        assert good.text == part_number


@then(parsers.parse('All goods have control code "{control_code}"'))
def good_control_code_is_found(driver, control_code):
    goods_list = ApplicationGoodsList(driver).get_good_control_codes()
    assert len(goods_list) > 0
    for good in goods_list:
        assert good.text == control_code


@then(parsers.parse('"{total}" goods are found'))
def total_goods_found(driver, total):
    total_goods = len(ApplicationGoodsList(driver).get_good_descriptions())
    assert total_goods == int(total), "Incorrect number of goods matching search criteria were found"


@when("I click the add from organisations goods button")  # noqa
def click_add_from_organisation_button(driver):  # noqa
    driver.find_element_by_css_selector('a[href*="add-preexisting"]').click()
