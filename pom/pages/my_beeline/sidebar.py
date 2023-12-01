from playwright.sync_api import Page, Locator
from pom.page_factory.description import Description
from pom.page_factory.link import Link


class SideBar:
    def __init__(self, page: Page, parent_locator: Locator) -> None:
        self.page = page
        self.name = 'Мой билайн: сайдбар'
        self._container = parent_locator.locator('[class*=sidebar]')

        self.phone_number = Description(self.page, self._container.locator('[class*=ctn]'), f'{self.name}: номер телефона')

        self._navigation_container = self._container.locator('[class*=Navigation_desktop]')
        self.nav_main_link = Link(self.page, self._navigation_container.get_by_text('Главная'), 'Главная')
        self.nav_home_link = Link(self.page, self._navigation_container.get_by_text('Мой билайн'), 'Мой билайн')
        self.connected_services_link = Link(self.page, self._navigation_container.get_by_text('Подключенные услуги'), 'Подключенные услуги')
        self.details_link = Link(self.page, self._navigation_container.get_by_text('Детализация'), 'Детализация')
        self.notifications_link = Link(self.page, self._navigation_container.get_by_text('Уведомления'), 'Уведомления')
        self.settings_link = Link(self.page, self._navigation_container.get_by_text('Настройки'), 'Настройки')
        self.mobile_id_link = Link(self.page, self._navigation_container.get_by_text('Мобильный ID'), 'Мобильный ID')
        self.settings_link = Link(self.page, self._navigation_container.get_by_text('Семья в билайне'), 'Семья в билайне')
