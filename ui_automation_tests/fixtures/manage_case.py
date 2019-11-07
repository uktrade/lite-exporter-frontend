from pytest import fixture

from shared.tools.utils import get_lite_client


@fixture(scope="module")
def manage_case_status(driver, seed_data_config, context):
    lite_client = get_lite_client(context, seed_data_config)
    status = lite_client.manage_case_status(context.app_id)
    assert status == 200, "Case status not updated to new status"
