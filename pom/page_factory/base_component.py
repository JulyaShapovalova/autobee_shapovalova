from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
import allure
from playwright.sync_api import Locator, Page, expect, Error
from lib.helpers.assertion import Assertion as assertion


class BaseComponent(ABC):
    def __init__(self, page: Page, locator: Locator, name: str) -> None:
        self._page = page
        self.name = name
        self.locator = locator

    @property
    @abstractmethod
    def type_of(self) -> str:
        return 'компонент'

    def get_locator(self) -> Locator:
        return self.locator

    def click(self, **kwargs) -> None:
        with allure.step(f'Кликнуть: {self.type_of} "{self.name}"'):
            self.locator.click(**kwargs)

    def click_until_element_visible(self, element_to_be_visible: BaseComponent, attempts_limit: int = 5) -> None:
        """
        Нажимает на элемент до того момента, пока не появится целевой элемент, либо попытки не будут исчерпаны.
        :param element_to_be_visible:
        :param attempts_limit:
        :return:
        """
        attempts = 0
        while True:
            try:
                self.click()
                element_to_be_visible.should_be_visible(timeout=3000)
                break
            except:
                attempts = attempts + 1
            if attempts >= attempts_limit:
                raise Error(f'Не удалось загрузить {element_to_be_visible.type_of} {element_to_be_visible.name} после {attempts} попыток')

    def focus(self, **kwargs) -> None:
        with allure.step(f'Сфокусироваться: {self.type_of} "{self.name}"'):
            self.locator.focus(**kwargs)

    def nth(self, index: int) -> Locator:
        with allure.step(f'Получить {index} {self.type_of} "{self.name}"'):
            return self.locator.nth(index)

    def get_text(self, **kwargs) -> str:
        with allure.step(f'Получить текст: {self.type_of} {self.name}'):
            return self.locator.inner_text(**kwargs)

    def get_all_text_contents(self) -> List[str]:
        with allure.step(f'Получить текст всех подходящих под условие локаторов: {self.type_of} "{self.name}"'):
            return self.locator.all_text_contents()

    def get_attribute(self, attribute: str, **kwargs) -> str:
        with allure.step(f'Получить значение атрибута {attribute}: {self.type_of} {self.name}'):
            return self.locator.get_attribute(attribute, **kwargs)

    def get_value_of_css_property(self, css_property: str, **kwargs) -> str:
        with allure.step(f'Получить значение css-свойства {css_property}: {self.type_of} {self.name}'):
            script = '(el) => {return window.getComputedStyle(el).getPropertyValue("%s")}' % css_property
            return self.locator.evaluate(script, **kwargs)

    def should_be_visible(self, **kwargs) -> None:
        with allure.step(f'Проверить: {self.type_of} "{self.name}" – видимо'):
            expect(self.locator).to_be_visible(**kwargs)

    def should_not_be_visible(self, **kwargs) -> None:
        with allure.step(f'Проверить: {self.type_of} "{self.name}" – невидимо'):
            expect(self.locator).not_to_be_visible(**kwargs)

    def should_be_enabled(self, **kwargs) -> None:
        with allure.step(f'Проверить: {self.type_of} "{self.name}" – доступно'):
            expect(self.locator).to_be_enabled(**kwargs)

    def should_be_disabled(self, **kwargs) -> None:
        with allure.step(f'Проверить: {self.type_of} "{self.name}" – недоступно'):
            expect(self.locator).to_be_disabled(**kwargs)

    def should_have_text(self, expected_value: str, **kwargs) -> None:
        with allure.step(f'Проверить: {self.type_of} "{self.name}" содержит текст "{expected_value}"'):
            expect(self.locator).to_have_text(expected_value, **kwargs)

    def should_have_all_text_contents(self, expected_value: str) -> None:
        with allure.step(f'Проверить: все совпадающие локаторы "{self.name}" имеют общее текстовое значение "{expected_value}"'):
            actual_value = ' '.join(self.get_all_text_contents())
            assertion.equal(actual_value, expected_value, f'Общее значение совпадает с ожидаемым)')

    def should_have_attribute(self, attribute: str, expected_value: str, **kwargs) -> None:
        with allure.step(f'Проверить атрибут {attribute}: {self.type_of} "{self.name}" имеет значение {expected_value}'):
            expect(self.locator).to_have_attribute(attribute, expected_value)

    def should_have_class(self, expected_class, **kwargs) -> None:
        with allure.step(f'Проверить: {self.type_of} "{self.name}" имеет класс {expected_class}'):
            expect(self.locator).to_have_class(expected_class, **kwargs)

    def should_have_css_property(self, css_property: str, expected_value: str, **kwargs) -> None:
        with allure.step(f'Проверить свойство {css_property}: {self.type_of} "{self.name}" имеет значение {expected_value}'):
            expect(self.locator).to_have_css(css_property, expected_value, **kwargs)
