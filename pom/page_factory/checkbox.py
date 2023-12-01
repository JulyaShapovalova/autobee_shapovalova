import allure
from playwright.sync_api import expect
from pom.page_factory.base_component import BaseComponent


class Checkbox(BaseComponent):
    @property
    def type_of(self) -> str:
        return 'чекбокс'

    def should_be_checked(self, **kwargs) -> None:
        with allure.step(f'Проверить: {self.type_of} "{self.name}" – выбран'):
            expect(self.locator).to_be_checked(**kwargs)
