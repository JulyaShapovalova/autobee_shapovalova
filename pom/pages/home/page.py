from playwright.sync_api import Page
from pom.page_factory.block import Block
from pom.pages.base_page import BasePage
import pom.shared_components.main_header.header as header


class HomePage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page, path='/customers/products/', name='Главная')
        self.page = page
        self.header = header.MainHeader(self, self._main_wrapper)
        self.lk_widget = Block(self.page, self.page.locator('#block_personal_info'), 'Виджет ЛК')
