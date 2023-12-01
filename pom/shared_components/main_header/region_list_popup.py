import os
import allure
from playwright.sync_api import Page, Locator, expect
from lib.helpers import url_helper
from pom.page_factory.button import Button
from pom.page_factory.input import Input
from pom.page_factory.link import Link
from pom.page_factory.title import Title
from pom.pages.base_page import BasePage
from pom.shared_components.modal import Modal


class RegionListPopup(Modal):
    def __init__(self, page: Page, parent_locator: Locator = None) -> None:
        super().__init__(page, 'Заявка на подключение', parent_locator)
        self.page = page
        self._container = parent_locator.locator('.content-inner')

        self.close_button = Button(self.page, self._container.locator('button'), 'Закрыть')

        self._search_container = self._container.locator('xpath=./*')
        self.title = Title(self.page, self._search_container.locator('h3'), 'Выбор региона')
        self.search_input = Input(self.page, self._search_container.locator('input'), 'Найти город')

        self._search_result_container = self._search_container.locator('xpath=./following-sibling::*')

    def select_region(self, region_name: str, region_alias: str, entry_page: BasePage) -> BasePage:
        with allure.step(f'Выбрать регион "{region_name}"'):
            current_region = url_helper.get_region(self.page.url)
            self.close_button.should_be_enabled()
            region_link = Link(self.page, self._search_result_container.locator(f'xpath=.//a[text()="{region_name}"]'), f'Регион {region_name}')
            region_link.click()
            expect(self._search_result_container).not_to_be_visible(), 'Попап выбора региона не был скрыт!'
            domain = url_helper.get_domain_without_region(os.getenv('BASE_URL'))
            os.environ['BASE_URL'] = f'https://{region_alias}.{domain}'
            entry_page._page_url = entry_page._page_url.replace(current_region, region_alias)
            entry_page.should_have_correct_url()
            return entry_page

    def search_region(self, region_name: str) -> Page:
        with allure.step(f'Найти регион {region_name}'):
            self.search_input.fill(region_name)
            expect(self._search_result_container.locator(f'xpath=.//*[text()="А"]')).not_to_be_visible(), 'Список регионов по алфавиту не был скрыт!'
            region_link = Link(self.page, self._search_result_container.locator(f'xpath=.//a[.//b[text()="{region_name}"]]'), f'Регион {region_name}')
            region_link.click()
            expect(self._search_result_container).not_to_be_visible(), 'Попап выбора региона не был скрыт!'
            return self.page
