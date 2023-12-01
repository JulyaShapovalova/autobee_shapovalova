import allure
from playwright.sync_api import Response
from lib.helpers.url_helper import get_url_without_query_params


class Assertion:
    @staticmethod
    def equal(actual: str | int | bool | list | tuple, expected: str | int | bool | list | tuple, check_name: str = None) -> None:
        with allure.step(f'Проверить: {check_name}: фактическое значение {actual} равно {expected}'):
            assert actual == expected, f'{actual} не равно {expected}'

    @staticmethod
    def greater_than(actual: str | int | bool | list | tuple, expected: str | int | bool | list | tuple, check_name: str = None) -> None:
        with allure.step(f'Проверить: {check_name}: фактическое значение {actual} больше {expected}'):
            assert actual > expected, f'{actual} меньше или равно {expected}'

    @staticmethod
    def greater_than_or_equal(actual: str | int | bool | list | tuple, expected: str | int | bool | list | tuple, check_name: str = None) -> None:
        with allure.step(f'Проверить: {check_name}: фактическое значение {actual} больше или равно {expected}'):
            assert actual >= expected, f'{actual} меньше {expected}'

    @staticmethod
    def less_than(actual: str | int | bool | list | tuple, expected: str | int | bool | list | tuple, check_name: str = None) -> None:
        with allure.step(f'Проверить: {check_name}: фактическое значение {actual} меньше {expected}'):
            assert actual < expected, f'{actual} больше или равно {expected}'

    @staticmethod
    def less_than_or_equal(actual: str | int | bool | list | tuple, expected: str | int | bool | list | tuple, check_name: str = None) -> None:
        with allure.step(f'Проверить: {check_name}: фактическое значение {actual} меньше или равно {expected}'):
            assert actual <= expected, f'{actual} больше {expected}'

    @staticmethod
    def to_be_true(statement: str | int | bool | list | tuple, check_name: str) -> None:
        with allure.step(f'Проверить: {check_name}: истина'):
            assert statement

    @staticmethod
    def to_be_false(statement: str | int | bool | list | tuple, check_name: str) -> None:
        with allure.step(f'Проверить: {check_name}: ложь'):
            assert statement == False

    @staticmethod
    def response_to_be_ok(response: Response):
        status = response.status
        with allure.step(f'Проверить: ответ запроса {get_url_without_query_params(response.url)} успешен – статус: {status}'):
            assert response.ok
