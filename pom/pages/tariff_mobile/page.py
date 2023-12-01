from playwright.sync_api import Page
from pom.pages.base_page import BasePage
from pom.shared_components.main_header import header


class TariffMobilePage(BasePage):
    def __init__(self, page: Page, tariff_name: str, alias: str) -> None:
        super().__init__(
            page,
            path=f'/customers/products/mobile/tariffs/details/{alias}/',
            name=f'Страница тарифа {tariff_name}'
        )
        self.page = page
        self.header = header.MainHeader(self, self._main_wrapper)
