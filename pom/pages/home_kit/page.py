import os
import allure
from playwright.sync_api import Page
from lib.helpers import url_helper
from lib.helpers.assertion import Assertion as assertion
from pom.page_factory.block import Block
from pom.page_factory.button import Button
from pom.page_factory.description import Description
from pom.page_factory.image import Image
from pom.page_factory.link import Link
from pom.page_factory.tab import Tab
from pom.pages.home_kit.data import *
from pom.shared_components.modal import Modal
from pom.pages.base_page import BasePage
import pom.shared_components.main_header.header as header
from pom.shared_components.tariff_catalogues.tariff_card_list import TariffCardList


class HomeKitPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page, path='/customers/products/home/kit/', name="Домашний интернет и ТВ")
        self.page = page
        self.header = header.MainHeader(self, self._main_wrapper)
        self.activation_request_modal = Modal(self.page, 'Заявка на подключение', self._page_wrapper)

        self._content_container = self._page_wrapper.locator('.mainContainer')

        self._heading_block_container = self._page_wrapper.locator('[data-t-id=blocks-HeadingBlock]')

        self._tariffs_section = self._content_container.locator('xpath=.//section[./*[@data-t-id="common-ContentLiner"]]')
        self._tariffs_heading_container = self._tariffs_section.locator('[data-t-id*=TariffsBlockHeading]')
        self._tariffs_tabs_container = self._tariffs_section.locator('[data-component=Tabs]')
        self._tariffs_catalogue_container = self._tariffs_section.locator('[data-t-id=common-ScrollContainerV3]')

        self.internet_tab = Tab(self.page, self._tariffs_tabs_container.locator(f'xpath=.//*[@data-component="Tab" and .//*[text()="{INTERNET_TAB_TITLE}"]]'), INTERNET_TAB_TITLE)

        self._available_in_cities_title_container = self._page_wrapper.locator(f'xpath=.//*[./*[text()="{AVAILABLE_IN_CITIES_TITLE}"]]')
        self._available_city_list_container = self._available_in_cities_title_container.locator('xpath=./following-sibling::*[@data-t-id="components-ColumnsList"]')
        self._available_city_links = self._available_city_list_container.locator(f'xpath=.//a')
        self.show_more_or_hide_button = Button(self.page, self._available_city_list_container.locator('xpath=./following-sibling::button'), f'{SHOW_MORE_BUTTON_TEXT}/{HIDE_BUTTON_TEXT}')

        self._banner_container = self._page_wrapper.locator('[data-t-id*=Banner]')
        self.no_internet_banner_img = Image(self.page, self._banner_container.locator('img'), 'Котик с лупой')
        self.no_internet_banner_description = Description(self.page, self._banner_container.locator('[data-component=Text]'), 'Баннер доступных регионов')

        self._mobile_tariffs_container = self._page_wrapper.locator('[data-t-id*=TariffsSwiper]')

    @property
    def _tariffs_block(self) -> Block:
        return Block(self.page, self._tariffs_section, 'Тарифы')

    @property
    def _mobile_tariffs_block(self) -> Block:
        return Block(self.page, self._mobile_tariffs_container, 'Мобильные тарифы')

    @property
    def tariff_cards(self) -> TariffCardList:
        return TariffCardList(self, self._tariffs_block, 'home')

    @property
    def mobile_tariff_cards(self) -> TariffCardList:
        return TariffCardList(self, self._mobile_tariffs_block)

    def get_available_region(self, region_name: str) -> Link:
        with allure.step(f'Получить ссылку региона "{region_name}"'):
            return Link(self.page, self._available_city_links.filter(has_text=region_name), f'Регион {region_name}')

    def get_available_regions_count(self) -> int:
        with allure.step(f'Получить количество доступных регионов'):
            return self._available_city_links.count()

    def to_internet_tariffs(self) -> None:
        with allure.step(f'Нажать на вкладку {INTERNET_TAB_TITLE}'):
            self.internet_tab.click()
            self.internet_tab.should_be_selected()

    def select_available_region(self, region_name: str, region_alias: str, region_change_required: bool = True) -> BasePage:
        with allure.step(f'Выбрать регион "{region_name}"'):
            current_region = url_helper.get_region(self.page.url)
            domain = url_helper.get_domain_without_region(os.getenv('BASE_URL'))
            if region_change_required:
                os.environ['BASE_URL'] = f'https://{region_alias}.{domain}'
                self._page_url = self._page_url.replace(current_region, region_alias)
            region_link = self.get_available_region(region_name)
            region_link.click()
            if region_change_required:
                self.should_have_correct_url()
            else:
                self.should_have_url(self._page_url.replace(current_region, region_alias))
            return self

    def show_more_available_regions(self) -> None:
        with allure.step(f'Показать все доступные регионы'):
            self.show_more_or_hide_button.should_have_text(SHOW_MORE_BUTTON_TEXT)
            before_count = self.get_available_regions_count()
            self.show_more_or_hide_button.click()
            after_count = self.get_available_regions_count()
            self.show_more_or_hide_button.should_have_text(HIDE_BUTTON_TEXT)
            assertion.greater_than(after_count, before_count, f'Количество регионов после нажатия увеличилось с {before_count}')

    def hide_available_regions(self) -> None:
        with allure.step(f'Скрыть дополнительные доступные регионы'):
            self.show_more_or_hide_button.should_have_text(HIDE_BUTTON_TEXT)
            before_count = self.get_available_regions_count()
            self.show_more_or_hide_button.click()
            after_count = self.get_available_regions_count()
            self.show_more_or_hide_button.should_have_text(SHOW_MORE_BUTTON_TEXT)
            assertion.less_than(after_count, before_count, f'Количество регионов после нажатия уменьшилось с {before_count}')

