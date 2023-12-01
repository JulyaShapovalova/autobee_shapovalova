import allure

_ZEPHYR_URL = 'https://servicedesk.veon.com/secure/Tests.jspa#/testCase'


def add_test_info(test_id: int, author: dict[str, str], func) -> None:
    allure.id(test_id)
    allure.link(f'{_ZEPHYR_URL}/B2CTEST-{test_id}')
    allure.testcase(test_id)
    allure.label("owner", author)
