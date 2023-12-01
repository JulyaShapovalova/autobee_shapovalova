import allure
from playwright.sync_api import Page, Locator
from lib.helpers.phone_numbers_helper import mobile_ctn_beautifier
from pom.page_factory.button import Button
from pom.page_factory.image import Image
from pom.page_factory.input import Input
from pom.page_factory.tab import Tab
from pom.pages.service_mobile.data import *
from pom.shared_components.modal import Modal


class ServiceActivationPopupUnauthorized(Modal):
    def __init__(self, page: Page, parent_locator: Locator = None) -> None:
        super().__init__(page, 'Подключение услуги (НЗ)', parent_locator)
        self.page = page

        self._tabs = self.locator.locator('[data-component=Tab]')
        self.sms_code_tab = Tab(self.page, self._tabs.filter(has_text=UNAUTH_GET_SMS_CODE_TAB_TEXT),
                                UNAUTH_GET_SMS_CODE_TAB_TEXT)
        self.login_tab = Tab(self.page, self._tabs.filter(has_text=UNAUTH_FILL_LOG_PASS_TAB_TEXT),
                             UNAUTH_FILL_LOG_PASS_TAB_TEXT)
        self.get_a_call_tab = Tab(self.page, self._tabs.filter(has_text=UNAUTH_CALL_THE_NUMBER), UNAUTH_CALL_THE_NUMBER)

        self._sms_login_form = self.locator.locator('.smsForm')
        self.phone_input = Input(self.page, self._sms_login_form.locator('[name=phone]'), 'Номер телефона')
        self.submit_button = Button(self.page, self._sms_login_form.locator('[type=submit]'), 'Подтверждение')
        self._captcha_container = self._sms_login_form.locator('[data-t-id*=Captcha]')
        self.captcha_image = Image(self.page, self._captcha_container.locator('img'), 'Каптча')
        self.captcha_value_input = Input(self.page, self._captcha_container.locator('#captchaKey'), 'Значение каптчи')
        self.captcha_input = Input(self.page, self._captcha_container.locator('[name=Captcha]'), 'Каптча')

    def fill_phone_number(self, ctn: str) -> None:
        with allure.step(f'Заполнить номер телефона: {ctn}'):
            self.phone_input.fill(ctn)
            self.phone_input.should_have_value(mobile_ctn_beautifier(ctn, spaces_only=True))

    def send_code(self, ctn: str) -> None:
        with allure.step(f'Отправить смс-код на номер {ctn}'):
            self.fill_phone_number(ctn)
            self.submit_button.should_have_text(UNAUTH_SEND_CODE_BUTTON_TEXT)
            self.submit_button.click()
            self.captcha_image.should_be_visible()

    def fill_captcha(self, captcha: str, correct: bool = True) -> None:
        with allure.step(f'Заполнить поле ввода каптчи: {captcha}'):
            self.submit_button.should_be_disabled()
            self.submit_button.should_have_text(UNAUTH_SEND_BUTTON_TEXT)
            self.captcha_input.fill(captcha)
            self.submit_button.click()
            if not correct:
                self.captcha_input.should_have_value('')

    def should_have_tabs(self):
        with allure.step('Проверить: все необходимые вкладки отображаются'):
            self.sms_code_tab.should_be_visible()
            self.login_tab.should_be_visible()
            self.get_a_call_tab.should_be_visible()
