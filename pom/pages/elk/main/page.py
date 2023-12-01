import allure
from playwright.sync_api import Page
from pom.page_factory.button import Button
from pom.page_factory.description import Description
from pom.page_factory.input import Input
from pom.page_factory.title import Title
from pom.pages.base_page import BasePage
import pom.shared_components.main_header.header as header
from pom.pages.basket.page import BasketPage
from pom.pages.elk.elk_sidebar import ElkSideBar
from pom.pages.elk.main.data import MNP_BUTTON_TEXT
from pom.pages.elk.top_menu import ElkTopMenu


class ElkPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page, path='/customers/products/elk/', name="ЕЛК")
        self.page = page

        self.header = header.MainHeader(self, self._main_wrapper)
        self.side_bar = ElkSideBar(self.page, self._page_wrapper)
        self.top_menu = ElkTopMenu(self.page, self._main_content)

        self._mobile_elk_block = self._main_content.locator('xpath=.//section[.//*[contains(@src,"mobile_elk")]]')
        self.mobile_tariff_button = Button(self.page, self._mobile_elk_block.locator('xpath=.//a[./*[text()="Подробнее"] and not(@data-name)]'), 'Блок мобильного тарифа')
        self._mnp_container = self._mobile_elk_block.locator('xpath=.//*[@data-component="Card" and .//a[contains(@href,"mnp")]]')
        self.mnp_block_title = Title(self.page, self._mnp_container.locator('[data-component=Text]'), 'Блок MNP')
        self._mnp_input_container = self._mnp_container.locator('[data-component=Input]')
        self.mnp_number_input = Input(self.page, self._mnp_input_container.locator('input'), 'Номер телефон для переноса')
        self.mnp_error_message = Description(self.page, self._mnp_input_container.locator('xpath=.//*[text()]'), 'Валидация при переносе')
        self.to_mnp_button = Button(self.page, self._mnp_container.locator('[type=submit]'), MNP_BUTTON_TEXT)

        self._home_elk_block = self._main_content.locator('xpath=.//section[.//*[contains(@src,"home_elk")]]')
        self.home_tariff_button = Button(self.page, self._home_elk_block.locator('xpath=.//a[./*[text()="Подробнее"] and not(@data-name)]'), 'Блок домашнего тарифа')

        self._eshop_elk_block = self._main_content.locator('xpath=.//section[.//*[contains(@src,"e-shop")]]')

    def fill_phone_number(self, number: str) -> None:
        with allure.step(f'Ввести номера для переноса: {number}'):
            self.mnp_number_input.fill(number)

    def proceed_to_mnp(self, number: str, error_expected: bool = False, click_required: bool = True) -> BasketPage | Description:
        error_expected_message = '(ожидается ошибка)' if error_expected else ''
        with allure.step(f'Перейти к процессу переноса номера {error_expected_message}'):
            self.fill_phone_number(number)
            if click_required:
                self.to_mnp_button.click()
            if error_expected:
                return self.mnp_error_message
            basket_page = BasketPage(self.page)
            basket_page.should_have_correct_url()
            return basket_page
