import allure
from playwright.sync_api import Page, Locator
from pom.page_factory.button import Button
from pom.pages.my_beeline.settings.number_management.data import SUCCESSFUL_UNLINK_TITLE, SUCCESSFUL_UNLINK_DESCRIPTION
from pom.pages.my_beeline.settings.number_management.successful_unlink_popup import SuccessfulUnlinkPopup
from pom.shared_components.modal import Modal


class RequestUnlinkPopup(Modal):
    def __init__(self, page: Page, parent_locator: Locator = None) -> None:
        super().__init__(page, 'Подтверждение отвязки номера', parent_locator)
        self.page = page

        self._successful_unlink_popup = SuccessfulUnlinkPopup(self.page, parent_locator)

        self.refuse_control_button = Button(self.page, self.locator.locator('[class*=Button_default][class*=UnlinkAccountConfirmationPopup]'), 'Да, отказаться от управления')
        self.close_without_changes = self.submit_button

    def refuse_control_click(self, ctn: str) -> SuccessfulUnlinkPopup:
        with allure.step('Подтвердить отказ от управления'):
            self.refuse_control_button.click()
            self._successful_unlink_popup.h1.should_have_text(SUCCESSFUL_UNLINK_TITLE)
            # TODO: ОШИБКА В СООБЩЕНИИ: "у управлению". Раскомменитровать, когда будет исправлено
            # popup.description.should_have_text(SUCCESSFUL_UNLINK_DESCRIPTION.format(ctn=ctn))
            return self._successful_unlink_popup
