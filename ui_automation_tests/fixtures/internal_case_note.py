from pytest import fixture
from helpers.seed_data import SeedData
from helpers.utils import get_or_create_attr


@fixture(scope="module")
def internal_case_note(driver,  api_url, context):
    api = get_or_create_attr(context, 'api', lambda: SeedData(api_url=api_url, logging=True))
    api.add_case_note(context, context.case_id)


@fixture(scope="module")
def internal_case_note_end_user_advisory(driver,  api_url, context):
    api = get_or_create_attr(context, 'api', lambda: SeedData(api_url=api_url, logging=True))
    api.add_case_note(context, context.end_user_advisory_case_id)
