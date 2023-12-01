from playwright.sync_api import Page, Locator
from pom.shared_components.modal import Modal


class ServiceActivationPopupAuthorized(Modal):
    def __init__(self, page: Page, parent_locator: Locator = None) -> None:
        super().__init__(page, 'Подключение услуги (АЗ)', parent_locator)
        self.page = page

    def should_have_some_expectation(self):
        pass
