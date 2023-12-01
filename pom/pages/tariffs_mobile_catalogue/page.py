import allure
from playwright.sync_api import Page
from pom.page_factory.block import Block
from pom.page_factory.button import Button
from pom.page_factory.description import Description
from pom.page_factory.link import Link
from pom.pages.base_page import BasePage
import pom.shared_components.main_header.header as header
from pom.pages.tariffs_mobile_catalogue.data import *
from pom.shared_components.tariff_catalogues.tariff_card import TariffCard
from pom.shared_components.tariff_catalogues.tariff_card_list import TariffCardList


class TariffsMobileCatalogue(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page, path='/customers/products/mobile/tariffs/', name='Каталог мобильных тарифов')
        self.page = page
        self.header = header.MainHeader(self, self._main_wrapper)

        # Блоки авторизованной зоны
        self._personal_tariffs_wrapper = self._page_wrapper.locator('.extended')

        self._current_tariff_card_container = self._personal_tariffs_wrapper.locator(f'xpath=.//*[./*[@data-component="Text" and text()="{MY_TARIFF_TITLE}"]]/following-sibling::*')
        self.current_tariff_link = Link(self.page, self._current_tariff_card_container.locator('xpath=.//a[not(@data-component)]'), MY_TARIFF_TITLE)
        self.current_tariff_name = Description(self.page, self._current_tariff_card_container.locator('[class*=top-wrapper] h3[data-component=Text]'), MY_TARIFF_TITLE)

        self._recommended_tariff_card_container = self._personal_tariffs_wrapper.locator(f'xpath=.//*[./*[@data-component="Text" and text()="{RECOMMENDED_FOR_YOU_TITLE}"]]/following-sibling::*')
        self.recommended_tariff_link = Link(self.page, self._recommended_tariff_card_container.locator('xpath=.//a[not(@data-component)]'), RECOMMENDED_FOR_YOU_TITLE)
        self.recommended_tariff_name = Description(self.page, self._recommended_tariff_card_container.locator('[class*=top-wrapper] h3[data-component=Text]'), RECOMMENDED_FOR_YOU_TITLE)

        # Блоки неавторизованной зоны
        self._tariffs_up_container = self._page_wrapper.locator('//*[@data-t-id="components-Group" and .//*[contains(text(),"UP")]]')

        self._tariffs_home_price_container = self._page_wrapper.locator(f'//*[@data-t-id="components-Group" and .//*[text()="{HOME_PRICE_TARIFFS_TITLE}"]]')

        self._application_container = self._page_wrapper.locator(f'//section[.//*[text()="{APPLICATION_BEELINE_BLOCK_TITLE}"]]')

        # Общие блоки
        self._more_tariffs_container = self._page_wrapper.locator(f'//*[@data-t-id="components-Group" and .//*[text()="{MORE_TARIFFS_TITLE}"]]')
        self.show_rare_tariffs_link = Link(self.page, self._more_tariffs_container.locator('xpath=.//h2/following-sibling::*[@data-name="Link"]'), SHOW_RARE_TARIFFS_LINK_TEXT)

        self.show_all_button = Button(self.page, self._page_wrapper.get_by_text(SHOW_ALL_TARIFFS_BUTTON_TEXT), SHOW_ALL_TARIFFS_BUTTON_TEXT)

    @property
    def more_tariffs_block(self) -> Block:
        return Block(self.page, self._more_tariffs_container, MORE_TARIFFS_TITLE)

    @property
    def _tariffs_up_block(self) -> Block:
        return Block(self.page, self._tariffs_up_container, TARIFFS_UP_TITLE)

    @property
    def _tariffs_home_price_block(self) -> Block:
        return Block(self.page, self._tariffs_home_price_container, HOME_PRICE_TARIFFS_TITLE)

    @property
    def application_block(self) -> Block:
        return Block(self.page, self._application_container, APPLICATION_BEELINE_BLOCK_TITLE)

    @property
    def tariff_up_cards(self) -> TariffCardList:
        return TariffCardList(self, self._tariffs_up_block)

    @property
    def home_price_cards(self) -> TariffCardList:
        return TariffCardList(self, self._tariffs_home_price_block)

    @property
    def more_tariff_cards(self) -> TariffCardList:
        return TariffCardList(self, self.more_tariffs_block)

    def _get_current_tariff_name(self) -> str:
        with allure.step('Получить название подключенного тарифа'):
            return self.current_tariff_name.get_text()

    def _get_current_tariff_alias(self) -> str:
        with allure.step('Получить alias подключенного тарифа'):
            return ' '.join(self.current_tariff_link.get_attribute('href').split('/')).split()[-1]

    def _get_recommended_tariff_name(self) -> str:
        with allure.step('Получить название рекомендуемого тарифа'):
            return self.recommended_tariff_name.get_text()

    def _get_recommended_tariff_alias(self) -> str:
        with allure.step('Получить alias рекомендуемого тарифа'):
            return ' '.join(self.recommended_tariff_link.get_attribute('href').split('/')).split()[-1]

    def get_current_tariff_card(self) -> TariffCard:
        with allure.step('Получить карточку подключенного тарифа'):
            tariff_name = self._get_current_tariff_name()
            alias = self._get_current_tariff_alias()
            return TariffCard(self.page, self._personal_tariffs_wrapper, tariff_name, alias)

    def get_recommended_tariff_card(self) -> TariffCard:
        with allure.step('Получить карточку рекомендуемого тарифа'):
            tariff_name = self._get_recommended_tariff_name()
            alias = self._get_recommended_tariff_alias()
            return TariffCard(self.page, self._personal_tariffs_wrapper, tariff_name, alias)

    def show_all_tariffs_if_button_is_visible(self):
        with allure.step(f'Раскрыть список всех тарифов, если кнопка {SHOW_ALL_TARIFFS_BUTTON_TEXT} есть на странице'):
            starting_count = self.more_tariff_cards.cards_count
            try:
                with allure.step(f'Кнопка представлена на странице. Проверить: после клика количество карточек изменилось (стало больше, чем {starting_count})'):
                    self.show_all_button.click()
                    self.more_tariff_cards.should_have_count_greater_than(starting_count)
            except:
                with allure.step(f'Кнопка не представлена на странице. Проверить: количество карточек осталось прежним ({starting_count})'):
                    self.more_tariff_cards.should_have_count_equal(starting_count)
