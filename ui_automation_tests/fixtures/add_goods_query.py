from pytest import fixture

from shared.tools.utils import get_lite_client


@fixture(scope="function")
def add_goods_query(context, seed_data_config):
    lite_client = get_lite_client(context, seed_data_config=seed_data_config)
    lite_client.goods_queries.add_clc_good(lite_client.goods, lite_client.ecju_queries)
    context.goods_query_good_id = lite_client.context["goods_query_good_id"]
