from playwright.sync_api import Page, Locator
from pom.page_factory.description import Description
from pom.shared_components.modal import Modal


class SuccessfulUnlinkPopup(Modal):
    def __init__(self, page: Page, parent_locator: Locator = None) -> None:
        super().__init__(page, 'Подтверждение отвязки номера', parent_locator)
        self.page = page

        self.description = Description(self.page, self.locator.locator('h6'), 'Доступ отменён')
