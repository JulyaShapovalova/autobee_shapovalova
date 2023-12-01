import allure
from pom.page_factory.base_component import BaseComponent


class Button(BaseComponent):
    @property
    def type_of(self) -> str:
        return 'кнопка'

    def hover(self) -> None:
        with allure.step(f'Навести курсор: {self.type_of} "{self.name}"'):
            self.locator.hover()

    def double_click(self):
        with allure.step(f'Двойной клик: {self.type_of} "{self.name}"'):
            self.locator.dblclick()
