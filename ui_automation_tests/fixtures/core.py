from conf.settings import env
import os
import types
from selenium import webdriver
from pytest import fixture


@fixture(scope="session")
def context(request):
    class Context(object):
        pass

    return Context()


@fixture(scope="session")
def invalid_username(request):
    return "invalid@mail.com"


@fixture(scope='session')
def exporter_info(request):
    exporter_sso_email = env('TEST_EXPORTER_SSO_EMAIL')
    exporter_sso_password = env('TEST_EXPORTER_SSO_PASSWORD')
    first_name = 'Test'
    last_name = 'Lite'

    return {
        'email': exporter_sso_email,
        'password': exporter_sso_password,
        'first_name': first_name,
        'last_name': last_name
    }


@fixture(scope='session')
def internal_info(request):
    gov_user_email = env('TEST_SSO_EMAIL')
    gov_user_first_name, gov_user_last_name = env('TEST_SSO_NAME').split(' ')

    return {
        'email': gov_user_email,
        'first_name': gov_user_first_name,
        'last_name': gov_user_last_name
    }


@fixture(scope='session')
def s3_key(request):
    s3_key = env('TEST_S3_KEY')
    return s3_key


@fixture(scope='session')
def seed_data_config(request, exporter_info, internal_info, s3_key):
    api_url = request.config.getoption('--lite_api_url')
    return {
        'api_url': api_url,
        'exporter': exporter_info,
        'gov': internal_info,
        's3_key': s3_key
    }
