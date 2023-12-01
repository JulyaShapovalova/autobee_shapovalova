import allure
from playwright.sync_api import expect
from pom.page_factory.base_component import BaseComponent


class Input(BaseComponent):
    @property
    def type_of(self) -> str:
        return 'поле ввода'

    def fill(self, value: str) -> None:
        with allure.step(f'Заполнить: {self.type_of} "{self.name}" значением "{value}"'):
            self.locator.fill(value)

    def press_enter(self):
        with allure.step(f'Нажать:  клавишу Enter для {self.type_of} "{self.name}"'):
            self.locator.press('Enter')

    def get_value(self, **kwargs) -> str:
        with allure.step(f'Получить значение: {self.type_of} "{self.name}"'):
            return self.locator.input_value(**kwargs)

    def get_placeholder(self, **kwargs) -> str:
        with allure.step(f'Получить значение плэйсхолдера]: {self.type_of} "{self.name}"'):
            return self.locator.get_attribute('placeholder', **kwargs)

    def should_have_value(self, value: str) -> None:
        with allure.step(f'Проверить: {self.type_of} "{self.name}" имеет значение "{value}"'):
            expect(self.locator).to_have_value(value)

    def should_not_have_value(self, value: str) -> None:
        with allure.step(f'Проверить: {self.type_of} "{self.name}" не имеет значение "{value}"'):
            expect(self.locator).not_to_have_value(value)

    def should_have_border_color(self, expected_value: str) -> None:
        with allure.step(f'Проверить: рамки {self.type_of} "{self.name}" имеют цвет "{expected_value}"'):
            self.should_have_css_property('border-color', expected_value, timeout=3000)

    def should_have_placeholder(self, expected_value: str) -> None:
        with allure.step(f'Проверить: {self.type_of} "{self.name}" имеет значение плэйсхолдера "{expected_value}"'):
            expect(self.locator).to_have_attribute('placeholder', expected_value)
