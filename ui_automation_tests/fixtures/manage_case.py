from pytest import fixture

from shared.tools.utils import get_lite_client


@fixture
def manage_case_status_to_withdrawn(driver, seed_data_config, context):
    lite_client = get_lite_client(context, seed_data_config)
    status = lite_client.manage_case_status(context.app_id, "withdrawn")
    assert status == 200, "Case status not updated to new status"


@fixture
def approve_case(driver, seed_data_config, context):
    lite_client = get_lite_client(context, seed_data_config)
    status = lite_client.finalise_case(context.app_id, "approve")
    assert status == 200, "Case cannot be finalised"
