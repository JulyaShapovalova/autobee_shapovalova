import allure
from playwright.sync_api import Page
from pom.pages.base_page import BasePage
import pom.shared_components.main_header.header as header
from pom.page_factory.button import Button
from pom.pages.services_catalogue.service_card import ServiceCard


# TODO: РЕФАКТОРИНГ: реализовать работу со страницей каталога услуг по образу и подобию каталога тарифов:
#  списки карточек, карточки, поиск по списку и т.д.
class ServicesCataloguePage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page, path='customers/products/mobile/services/cellphone/', name='Услуги')
        self.page = page
        self.header = header.MainHeader(self, self._main_wrapper)
        self.show_all_services_button = Button(self.page, self._page_wrapper.locator("xpath=//*[text()='Показать все услуги']"), name='Показать все услуги')
        self._service_block = self._page_wrapper.locator("#catalog-grid")

    def get_service_card(self, service_name: str, alias: str) -> ServiceCard:
        with allure.step(f'Выбрать услугу {self.name}'):
            self.show_all_services_button.click()
            return ServiceCard(self.page, self._service_block, service_name, alias)



