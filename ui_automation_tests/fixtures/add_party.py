from pytest import fixture

from shared.tools.utils import get_lite_client


@fixture(scope="function")
def add_end_user_to_application(context, seed_data_config):
    lite_client = get_lite_client(context, seed_data_config=seed_data_config)
    lite_client.parties.add_end_user(context.draft_id)
    context.end_user = lite_client.context["end_user"]
