import allure
from pom.page_factory.base_component import BaseComponent


class Block(BaseComponent):
    @property
    def type_of(self) -> str:
        return 'блок'

    def should_have_background_color(self, expected: str) -> None:
        with allure.step(f'Проверить: цвет заливки ({self.type_of} "{self.name}") имеет значение {expected}'):
            self.should_have_css_property('background-color', expected, timeout=3000)
