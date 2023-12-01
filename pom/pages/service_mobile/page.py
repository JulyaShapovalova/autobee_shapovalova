import allure
from playwright.sync_api import Page
from pom.page_factory.button import Button
from pom.pages.base_page import BasePage
from pom.pages.login.page import LoginPage
from pom.pages.service_mobile.service_activation_popup_authorized import ServiceActivationPopupAuthorized
from pom.pages.service_mobile.service_activation_popup_unauthorized import ServiceActivationPopupUnauthorized
from pom.shared_components.main_header import header


class ServiceMobilePage(BasePage):
    def __init__(self, page: Page, name: str, alias: str, query_params: dict[str, ...] | None = None) -> None:
        super().__init__(
            page,
            path=f'/customers/products/mobile/services/details/{alias}',
            name=name,
            query_params=query_params
        )
        self.page = page
        self.header = header.MainHeader(self, self._main_wrapper)
        self.service_activation_popup_unauthorized = ServiceActivationPopupUnauthorized(self.page, self._page_wrapper)
        self.service_activation_popup_authorized = ServiceActivationPopupAuthorized(self.page, self._page_wrapper)

        self.activation_button = Button(self.page, self._page_wrapper.locator('button'), 'Подключить услугу')

    def to_activate(
            self,
            authorized_zone: bool = False,
            redirect_to_login: bool = False
    ) -> LoginPage | ServiceActivationPopupAuthorized | ServiceActivationPopupUnauthorized:
        with allure.step(f'Перейти к подключению услуги "{self.name}"'):
            self.activation_button.click()
            if redirect_to_login:
                path = self.get_path()
                login_page = LoginPage(self.page)
                # login_page.login_form.title.should_have_text(LOGIN_FORM_TITLE)
                login_page.should_have_correct_url(path)
                return login_page
            if authorized_zone:
                return self.service_activation_popup_authorized
            else:
                return self.service_activation_popup_unauthorized
