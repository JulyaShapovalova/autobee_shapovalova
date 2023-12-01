from playwright.sync_api import Page
from pom.page_factory.title import Title
from pom.pages.base_page import BasePage
import pom.shared_components.main_header.header as header


class FttbTariffPage(BasePage):
    def __init__(self, page: Page, alias: str) -> None:
        super().__init__(
            page,
            path=f'/customers/products/home/home-tariffs/tariffs/kit/{alias}',
            name=f'Информация о домашнем тарифе {alias}'
        )
        self.page = page
        self.header = header.MainHeader(self, self._main_wrapper)

        self._navigation_bar_container = self._page_wrapper.locator('[data-t-id=components-FamilyNavigation]').nth(0)

        self._details_container = self._page_wrapper.locator('section')
        self.title = Title(self.page, self._details_container.locator('h1'), 'Домашний тариф')
