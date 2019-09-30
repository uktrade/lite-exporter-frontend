from pytest import fixture

from helpers.utils import get_lite_client


@fixture(scope="module")
def internal_ecju_query(driver,  api_url, context, seed_data_config):
    lite_client = get_lite_client(context, api_url, seed_data_config=seed_data_config)
    lite_client.add_ecju_query(context.case_id)


@fixture(scope="module")
def internal_ecju_query_end_user_advisory(driver,  api_url, context, seed_data_config):
    lite_client = get_lite_client(context, api_url, seed_data_config=seed_data_config)
    lite_client.add_ecju_query(context.end_user_advisory_case_id)
