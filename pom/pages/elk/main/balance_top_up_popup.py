import allure
from playwright.sync_api import Page, Locator
from lib.helpers.phone_numbers_helper import mobile_ctn_beautifier
from pom.page_factory.button import Button
from pom.page_factory.description import Description
from pom.page_factory.input import Input
from pom.page_factory.tab import Tab
from pom.shared_components.modal import Modal


class BalanceTopUpPopup(Modal):
    def __init__(self, page: Page, parent_locator: Locator = None) -> None:
        super().__init__(page, 'Пополнение счёта', parent_locator)
        self.page = page

        self.tab_phone = Tab(self.page, self._tabs_form.locator('xpath=.//*[@data-component="Tab"][.//*[text()="Телефон"]]'), 'Телефон')
        self.tab_internet = Tab(self.page, self._tabs_form.locator('xpath=.//*[@data-component="Tab"][.//*[text()="Интернет"]]'), 'Интернет')

        self._phone_number_container = self._main_form.locator('xpath=.//*[@data-component="Input"][.//*[text()="Номер получателя"]]')
        self.phone_number_input = Input(self.page, self._phone_number_container.locator('input'), 'Номер получателя')

        self._amount_container = self._main_form.locator('xpath=.//*[@data-component="Input"][.//*[text()="Сумма"]]')
        self.amount_input = Input(self.page, self._amount_container.locator('input'), 'Сумма')
        self.amount_validation_message = Description(self.page, self._amount_container.locator('xpath=.//*[contains(text(),"сумма")]'), 'Валидационное сообщение')

        self._payment_method_select_container = self._main_form.locator('[data-component=Select]')
        self.select_opener_button = Button(self.page, self._payment_method_select_container.locator('xpath=.//button[./*]'), 'Открытие селекта')

    def should_have_phone_number(self, ctn):
        phone_number = mobile_ctn_beautifier(ctn, True)
        with allure.step(f'Проверить: номер телефона в поле ввода верный и соответствует маске – "{phone_number}"'):
            self.phone_number_input.should_have_value(phone_number)

    def should_have_payment_method(self, payment_method):
        with allure.step(f'Проверить: значение выбранного метода оплаты – "{payment_method}"'):
            self.select_opener_button.should_have_text(payment_method)
