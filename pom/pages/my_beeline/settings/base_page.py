import allure
from playwright.sync_api import Page
from pom.page_factory.tab import Tab
from pom.pages.my_beeline.base_page import MyBeelineBasePage
import pom.pages.my_beeline.settings.number_management.page as number_management


class SettingsBasePage(MyBeelineBasePage):
    def __init__(self, page: Page, path: str, name) -> None:
        super().__init__(page, path=path, name=name)
        self.page = page

        self._settings_navigation_container = self._page_wrapper.locator('[class*=Settings_navigation]')
        self.number_management_tab = Tab(self.page, self._settings_navigation_container.get_by_text('Управление номерами'), 'Управление номерами')
        self.notifications_tab = Tab(self.page, self._settings_navigation_container.get_by_text('Уведомления'), 'Уведомления')
        self.password_and_access_tab = Tab(self.page, self._settings_navigation_container.get_by_text('Пароль и доступ'), 'Пароль и доступ')
        self.user_form_tab = Tab(self.page, self._settings_navigation_container.get_by_text('Анкета абонента'), 'Анкета абонента')
        self.personal_data_tab = Tab(self.page, self._settings_navigation_container.get_by_text('Обновление персональных данных'), 'Обновление персональных данных')

    def to_number_management(self):
        with allure.step('Перейти: управление номерами'):
            self.number_management_tab.click()
            page = number_management.NumberManagementPage(self.page)
            page.should_have_correct_url()
            return page
