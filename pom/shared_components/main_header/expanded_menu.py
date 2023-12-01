import allure
from playwright.sync_api import Page, Locator
from pom.page_factory.block import Block
from pom.page_factory.button import Button
from pom.page_factory.link import Link
from pom.pages.tariffs_mobile_catalogue.page import TariffsMobileCatalogue
from pom.shared_components.main_header.data import *


class ExpandedMenu(Block):
    def __init__(self, page: Page, parent_locator: Locator) -> None:
        super().__init__(page, parent_locator.locator('nav'), 'Раскрытое меню')
        self.page = page

        self._sidebar_container = self.locator.locator('[aria-label]')
        self._content_container = self._sidebar_container.locator('xpath=./following-sibling::*')

        self._mobile_sidebar = self._sidebar_container.locator('xpath=./ul[.//a[contains(@href,"products")]]')
        self.mobile_button = Button(self.page, self._mobile_sidebar.get_by_text(MOBILE_TITLE), MOBILE_TITLE)

        self.home_internet_button = Button(self.page, self._mobile_sidebar.get_by_text(HOME_INTERNET_TITLE), HOME_INTERNET_TITLE)

        self._eshop_sidebar = self._sidebar_container.locator('xpath=./ul[.//a[contains(@href,"shop")]]')

        self._mobile_content_container = self._content_container.locator(f'xpath=.//ul[.//*[@data-component="Text" and text()="{MOBILE_TITLE}"]]')

        self._tariffs_container = self._mobile_content_container.locator(f'xpath=.//ul[.//*[@data-component="Text" and .//*[text()="{TARIFFS_TITLE}"]]]')
        self.smartphone_tariffs = Link(self.page, self._tariffs_container.locator(f'xpath=.//a[.//*[text()="{SMARTPHONE_TARIFFS_TITLE}"]]'), SMARTPHONE_TARIFFS_TITLE)

    def expand_mobile(self):
        with allure.step(f'Раскрыть меню: "{MOBILE_TITLE}"'):
            self.mobile_button.focus()

    def to_smartphone_tariffs(self) -> TariffsMobileCatalogue:
        with allure.step(f'Перейти: "{SMARTPHONE_TARIFFS_TITLE}"'):
            self.expand_mobile()
            self.smartphone_tariffs.click()
            page = TariffsMobileCatalogue(self.page)
            page.should_have_correct_url()
            return page
