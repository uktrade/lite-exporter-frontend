from pytest import fixture
from helpers.seed_data import SeedData
from helpers.utils import get_or_create_attr


@fixture(scope="module")
def internal_ecju_query(driver,  api_url, context):
    pass
