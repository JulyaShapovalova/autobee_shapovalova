import functools
import os
import allure
import pytest
from allure_commons.types import LinkType
from lib.data.test_cases import *

_ZEPHYR_URL = 'https://servicedesk.veon.com/secure/Tests.jspa#/testCase/B2CTEST'


def set_allure_info(test_case_id, custom_title=''):
    def decorator(test_method):
        @functools.wraps(test_method)
        def wrapper(self, *args, **kwargs):
            test_cases = list(filter(None, [tc.get(test_case_id) for tc in ALL_TEST_CASES]))
            test_case_url = f'{_ZEPHYR_URL}-{test_case_id}'
            if test_cases:
                test_case_data = test_cases[0]
                test_case_title = test_case_data['title'] if not custom_title else custom_title
                allure.dynamic.parameter('environment', os.getenv('ENV_NAME'))
                allure.dynamic.title(test_case_title)
                allure.dynamic.severity(test_case_data['severity'])
                allure.dynamic.link(url=test_case_url, name=test_case_id, link_type=LinkType.LINK)
                allure.dynamic.label('owner', f'Владелец тест-кейса: {test_case_data["owner"]}')
            else:
                raise ValueError(f'Информация о тест-кейсе {test_case_id} не найдена!')
            return test_method(self, *args, **kwargs)
        return wrapper
    return decorator


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        with allure.step("Скриншот"):
            allure.attach(item.funcargs["page"].screenshot(), name="screenshot",
                          attachment_type=allure.attachment_type.PNG)
