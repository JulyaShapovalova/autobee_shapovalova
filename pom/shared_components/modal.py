import allure
from playwright.sync_api import Page, expect, Locator
from pom.page_factory.block import Block
from pom.page_factory.button import Button
from pom.page_factory.title import Title


class Modal(Block):
    def __init__(self, page: Page, name: str, parent_locator: Locator = None) -> None:
        container = parent_locator.locator('xpath=.//*[@role and .//*[local-name()="svg"]]') if parent_locator else (
            page.locator('[data-component=Modal]'))
        super().__init__(page, container, 'Попап')
        self.page = page
        self.name = name

        self._container = self.locator
        self._tabs_form = self._container.locator('[data-component=Tabs]')
        self._main_form = self._container.locator('form')
        self.close_button = Button(self.page, self._container.locator('svg').first, 'Закрытие попапа')
        self.h1 = Title(self.page, self._container.locator('h1'), f'{self.type_of} "{self.name}"')
        self.h2 = Title(self.page, self._container.locator('h2'), f'{self.type_of} "{self.name}"')
        self.h3 = Title(self.page, self._container.locator('h3'), f'{self.type_of} "{self.name}"')
        self.submit_button = Button(self.page, self._container.locator('[type=submit]'), 'Подтверждение')

    @property
    def type_of(self) -> str:
        return 'попап'

    def close(self) -> None:
        with allure.step(f'Закрыть: {self.type_of} "{self.name}"'):
            self.close_button.click()
            self.should_not_be_visible()
