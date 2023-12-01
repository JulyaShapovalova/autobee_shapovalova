import typing
import allure
from playwright.sync_api import Page, Locator
from pom.page_factory.block import Block
from pom.page_factory.description import Description
from pom.page_factory.link import Link
from pom.page_factory.title import Title
from pom.pages.fttb_tariff.page import FttbTariffPage
from pom.pages.tariff_mobile.page import TariffMobilePage


# TODO: во время разработки тестов на подключение тарифа реализовать в общем классе метод подключения, удалив из FttbTariffCard
class TariffCard(Block):
    def __init__(
            self,
            page: Page,
            parent_locator: Locator,
            tariff_name: str = None,
            alias: str = None,
            index: int = None,
            tariff_type: typing.Optional[typing.Literal['mobile', 'home']] = 'mobile',
    ) -> None:
        if tariff_name:
            container = parent_locator.locator(f'xpath=.//*[./a[.//*[text()="{tariff_name}"]]]')
            name = tariff_name
        elif type(index) is int:
            container = parent_locator.locator('xpath=.//*[./a[.//*[text()] and not(@data-component)]]').nth(index)
            name = f'с номером {index}'
        else:
            raise AttributeError('Отсутствует один из атрибутов выбора карточки тарифа')
        super().__init__(page, container, f'Карточка тарифа {name}')
        self.page = page
        self._tariff_name = name
        self._alias = alias
        self._tariff_type = tariff_type
        self._base_href = None

        self.tariff_link = Link(self.page, self.locator.locator('a:not([data-component])'), f'Тариф {self._tariff_name}')
        self.tariff_title = Title(self.page, self.tariff_link.locator.locator('h1'), 'Карточка тарифа')

        self._footer_container = self.locator.locator('[class*=footer--default]')
        self.old_price = Description(self.page, self._footer_container.locator('[class*=sale]'), 'Старая цена')

    def select(self) -> TariffMobilePage | FttbTariffPage:
        with allure.step(f'Выбрать тариф {self._tariff_name}'):
            if self._tariff_type == 'mobile':
                page = TariffMobilePage(self.page, self._tariff_name, self._alias)
            elif self._tariff_type == 'home':
                page = FttbTariffPage(self.page, self._alias)
            self.tariff_link.click()
            page.should_have_correct_url()
            return page

    def get_name(self) -> str:
        with allure.step('Получить название тарифа'):
            return self.tariff_title.get_text()

    def get_alias(self) -> str:
        alias = ' '.join(self.tariff_link.locator.locator('a').get_attribute('href').split('/')).split()[-1]
        with allure.step(f'Получить alias карточки тарифа: {alias}'):
            return alias

    def should_have_name(self, name: str) -> None:
        with allure.step(f'Проверить: название тарифа верное – "{name}"'):
            self.tariff_title.should_have_text(name)
