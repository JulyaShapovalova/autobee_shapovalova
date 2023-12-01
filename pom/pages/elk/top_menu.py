import allure
from playwright.sync_api import Page, Locator
from pom.page_factory.block import Block
from pom.page_factory.tab import Tab
from pom.pages.my_beeline.settings.number_management.page import NumberManagementPage


class ElkTopMenu(Block):
    def __init__(self, page: Page, parent_locator: Locator) -> None:
        super().__init__(page, parent_locator.locator('ul'), 'Верхнее навигационное меню')
        self.page = page

        self.main_tab = Tab(self.page, self.locator.locator('xpath=.//a[./*[text()="Настройки"]]'), 'Настройки')
        self.messages_tab = Tab(self.page, self.locator.locator('xpath=.//a[./*[text()="Сообщения"]]'), 'Сообщения')
        self.mobile_tab = Tab(self.page, self.locator.locator('xpath=.//a[./*[text()="Мобильная связь"]]'), 'Мобильная связь')
        self.details_tab = Tab(self.page, self.locator.locator('xpath=.//a[./*[text()="Детализация"]]'), 'Детализация')
        self.notifications_tab = Tab(self.page, self.locator.locator('xpath=.//a[./*[text()="Уведомления"]]'), 'Уведомления')
        self.settings_tab = Tab(self.page, self.locator.locator('xpath=.//a[./*[text()="Настройки"]]'), 'Настройки')
        self.mobile_id_tab = Tab(self.page, self.locator.locator('xpath=.//a[./*[text()="Мобильный ID"]]'), 'Мобильный ID')

    def to_settings(self) -> NumberManagementPage:
        with allure.step('Перейти: настройки'):
            self.settings_tab.click()
            page = NumberManagementPage(self.page)
            page.should_have_correct_url()
            return page
