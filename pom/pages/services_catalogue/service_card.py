import allure
from playwright.sync_api import Page, Locator
from pom.page_factory.button import Button
from pom.page_factory.link import Link
from pom.pages.service_mobile.data import AUTO_CONNECTION_SIGN
from pom.pages.service_mobile.page import ServiceMobilePage
from pom.pages.service_mobile.service_activation_popup_authorized import ServiceActivationPopupAuthorized
from pom.pages.service_mobile.service_activation_popup_unauthorized import ServiceActivationPopupUnauthorized


class ServiceCard:
    def __init__(self, page: Page, parent_locator: Locator, service_name: str, alias: str):
        self.page = page
        self.service_name = service_name
        self.alias = alias
        self._container = parent_locator.locator('[role=presentation]').filter(has_text=f'{self.service_name}')
        self.service_link = Link(self.page, self._container.locator('a'), 'Карточка услуги')
        self.activation_button = Button(self.page, self._container.locator('[type=submit]'), 'Подключение услуги')

    def select(self) -> ServiceMobilePage:
        with allure.step(f'Выбрать услугу {self.service_name}'):
            service_mobile_page = ServiceMobilePage(self.page, self.service_name, self.alias)
            self.service_link.click()
            service_mobile_page.should_have_correct_url()
            return service_mobile_page

    def activate(
            self,
            authorized_zone: bool = False
    ) -> (ServiceMobilePage, ServiceActivationPopupAuthorized | ServiceActivationPopupUnauthorized):
        with allure.step(f'Нажать: {self.activation_button.type_of} {self.activation_button.name} "{self.service_name}"'):
            service_mobile_page = ServiceMobilePage(
                self.page, self.service_name, self.alias, {AUTO_CONNECTION_SIGN: 'true'}
            )
            if authorized_zone:
                popup = service_mobile_page.service_activation_popup_authorized
            else:
                popup = ServiceActivationPopupUnauthorized(service_mobile_page.page, service_mobile_page.page_wrapper)
            self.activation_button.click()
            service_mobile_page.should_have_correct_url()
            return service_mobile_page, popup
