import allure
from playwright.sync_api import Page, Locator
from pom.page_factory.description import Description
from pom.page_factory.title import Title
from pom.shared_components.tariff_catalogues.tariff_card import TariffCard


class MobileTariffCard(TariffCard):
    def __init__(self, page: Page, parent_locator: Locator, tariff_name: str = None, alias: str = None, index: int = None) -> None:
        super().__init__(page, parent_locator, tariff_name, alias, index, 'mobile')
        self.page = page
        self.name = tariff_name
        self._base_href = '/customers/products/mobile/tariffs/details/{alias}/'

        self.tariff_title = Title(self.page, self.tariff_link.locator.locator('h3'), 'Заголовок тарифа')

        self._footer_container = self.locator.locator('[class*=footer--default]')
        self.old_price = Description(self.page, self._footer_container.locator('[class*=sale]'), 'Старая цена')

    def should_have_discount(self) -> None:
        with allure.step(f'Проверить: блок старой цены {self.name} видим (есть скидка)'):
            self.old_price.should_be_visible()
