import allure
from playwright.sync_api import Page, Locator
from lib.helpers.phone_numbers_helper import mobile_ctn_beautifier
from pom.page_factory.description import Description
from pom.page_factory.link import Link
from pom.page_factory.table.row import TableRow
from pom.pages.my_beeline.preloader import PreloaderMyBeeline
from pom.pages.my_beeline.settings.base_page import SettingsBasePage
from pom.pages.my_beeline.settings.number_management.data import REQUEST_UNLINK_POPUP_TITLE, \
    EMPTY_ASSOCIATED_NUMBERS_MESSAGE
from pom.pages.my_beeline.settings.number_management.request_unlink_popup import RequestUnlinkPopup


class NumberManagementPage(SettingsBasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page, path='/customers/products/mobile/profile/#/settings/number-management', name='Настройки: управление номерами')
        self.page = page

        self._app_container = self._page_wrapper.locator('[class*=App_container]')
        self._data_blocks_container = self._page_wrapper.locator('[class*=DataBlocks_container]')

        self._request_unlink_popup = RequestUnlinkPopup(self.page, self._app_container)

        self._login_container = self._data_blocks_container.locator('.xpath=.//section[.//*[text()="Ваш логин"]]')

        self._connected_numbers_container = self._data_blocks_container.locator('xpath=.//section[.//*[text()="Привязанные номера"]]')
        self.connected_number_preloader = PreloaderMyBeeline(self.page, self._connected_numbers_container)
        self._connected_numbers_rows = self._connected_numbers_container.locator('xpath=.//table//tr[.//td[contains(@class,"phoneNumber")]]')
        self.empty_message = Description(self.page, self._connected_numbers_container.locator('[class*=emptyMessage]'), EMPTY_ASSOCIATED_NUMBERS_MESSAGE)

    def _get_connected_number_row(self, number: str) -> TableRow:
        with allure.step(f'Получить: строка с номером {number}'):
            return TableRow(self.page, self._connected_numbers_rows.locator('[class*=phoneNumber]').filter(has_text=number).locator('xpath=./parent::tr'), f'Привязанный номер {number}')

    def _unlink_click(self, number: str, row: TableRow) -> RequestUnlinkPopup:
        with allure.step('Перейти: попап отвязки номера'):
            unlink_link = Link(self.page, row.locator.get_by_text('Отвязать'), 'Отвязать')
            unlink_link.click()
            self._request_unlink_popup.h3.should_have_text(REQUEST_UNLINK_POPUP_TITLE.format(number=number))
            return self._request_unlink_popup

    def unlink_number(self, ctn: str, soft_number_search: bool = True) -> None:
        number = mobile_ctn_beautifier(ctn)
        with allure.step(f'Отвязать номер {number}'):
            self.connected_number_preloader.should_not_be_visible()
            try:
                self.empty_message.should_not_be_visible(timeout=5000)
            except:
                if soft_number_search:
                    print(f'Нет привязанных номеров')
                    pass
                else:
                    raise Exception(f'Нет привязанных номеров')
            try:
                row = self._get_connected_number_row(number)
                row.should_be_visible(timeout=10000)
                request_unlink_popup = self._unlink_click(number, row)
            except:
                if soft_number_search:
                    print(f'Номер {number} не был привязан')
                    pass
                else:
                    raise Exception(f'Номер {number} не был привязан')
            else:
                successful_popup = request_unlink_popup.refuse_control_click(ctn)
                successful_popup.close()
