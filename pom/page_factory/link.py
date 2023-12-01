import allure
from playwright.sync_api import expect
from pom.page_factory.base_component import BaseComponent


class Link(BaseComponent):
    @property
    def type_of(self) -> str:
        return 'ссылка'

    def should_have_href(self, href: str):
        with allure.step(f'Проверить: {self.type_of} "{self.name}" имеет значение "{href}"'):
            expect(self.locator).to_have_attribute('href', href)
