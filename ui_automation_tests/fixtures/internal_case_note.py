from pytest import fixture

from helpers.utils import get_lite_client


@fixture(scope='module')
def internal_case_note(context):
    lite_client = get_lite_client(context)
    lite_client.create_case_note()
    context.text = lite_client.context['text']
