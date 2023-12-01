import allure
from playwright.sync_api import expect
from pom.page_factory.base_component import BaseComponent


class Image(BaseComponent):
    @property
    def type_of(self) -> str:
        return 'изображение'

    def should_have_src(self, src: str):
        with allure.step(f'Проверить: {self.type_of} "{self.name}" имеет значение "{src}"'):
            expect(self.locator).to_have_attribute('src', src)
