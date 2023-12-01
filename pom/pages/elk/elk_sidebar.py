import os
import allure
from playwright.sync_api import Page, Locator
from lib.helpers.phone_numbers_helper import mobile_ctn_beautifier
from lib.helpers.assertion import Assertion as assertion
from pom.page_factory.block import Block
from pom.page_factory.button import Button
from pom.page_factory.description import Description
from pom.pages.elk.main.data import ACCOUNT_ADDING_POPUP_TITLE, TOP_UP_POPUP_TITLE, BALANCE_BLOCK_BACKGROUND_WHITE, \
    BALANCE_POSITIVE_BLOCK_BACKGROUND_YELLOW, BALANCE_NEGATIVE_BLOCK_BACKGROUND_RED
from pom.pages.elk.main.account_adding_popup import AccountAddingPopup
from pom.pages.elk.main.balance_top_up_popup import BalanceTopUpPopup


class ElkSideBar(Block):
    def __init__(self, page: Page, parent_locator: Locator) -> None:
        super().__init__(page, parent_locator.locator('aside'), 'Сайдбар ЕЛК')
        self.page = page

        self._info_card = self.locator.locator('[data-component=Card]')
        self._finance_block = self._info_card.locator('[data-testid=finance-desktop-view]')
        self.phone_number_button = Button(self.page, self._finance_block.locator('xpath=.//button[text()]'), 'Выбор аккаунта')
        self.balance_block = self._finance_block.locator('xpath=.//*[./*[contains(text(),"₽")]]/parent::*')
        self.balance_value = Description(self.page, self.balance_block.locator('xpath=.//*[contains(text(),"₽")]'), 'Значение баланса')
        self.top_up_balance_button = Button(self.page, self.balance_block.locator('xpath=.//button[./*[contains(translate(., "П", "п"), "пополнить")]]'), 'Пополнить баланс')
        self._bottom_block = self._finance_block.locator('xpath=./following-sibling::*[not(contains(@class,"hidden"))]')
        self.add_account_button = Button(self.page, self._bottom_block.locator(f'button:has-text("{ACCOUNT_ADDING_POPUP_TITLE}")'), ACCOUNT_ADDING_POPUP_TITLE)

    def get_card_phone_number(self) -> str:
        with allure.step('Получить: номер телефона из карточки'):
            return self.phone_number_button.get_text()

    def add_account_click(self) -> AccountAddingPopup:
        self.phone_number_button.click()
        self.add_account_button.click()
        popup = AccountAddingPopup(self.page)
        popup.title_message.should_have_text(ACCOUNT_ADDING_POPUP_TITLE)
        return popup

    def get_balance_value(self, digit: bool = False) -> str | float:
        with allure.step('Получить: значение баланса'):
            balance_value = self.balance_value.get_text()
            return float(
                balance_value.replace(' ', '').replace(',', '.').replace('₽', '')
            ) if digit else balance_value

    def to_top_up_balance(self) -> BalanceTopUpPopup:
        with allure.step('Перейти: пополнение баланса'):
            self.top_up_balance_button.click()
            popup = BalanceTopUpPopup(self.page)
            popup.h2.should_have_text(TOP_UP_POPUP_TITLE)
            return popup

    def should_have_phone_number(self, ctn) -> None:
        beautified_ctn = mobile_ctn_beautifier(ctn)
        with allure.step(f'Проверить: ctn "{ctn}" соответствует отформатированному номеру на карточке "{beautified_ctn}"'):
            self.phone_number_button.should_be_visible()
            self.phone_number_button.should_have_text(beautified_ctn)

    def should_have_positive_balance(self, is_positive: bool = True) -> None:
        """
        Метод проверки баланса на ПОЛОЖИТЕЛЬНОЕ/ОТРИЦАТЕЛЬНОЕ значение
        :param is_positive:
        :return:
        """
        balance_type_message = 'положительное' if is_positive else 'отрицательное'
        balance_value = self.get_balance_value(digit=True)
        message = f'Проверить: значение баланса – {balance_type_message}: {balance_value}'
        with allure.step(message):
            if is_positive:
                assertion.greater_than_or_equal(balance_value, 0, f'Значение {balance_type_message}')
            else:
                assertion.less_than(balance_value, 0, f'Значение {balance_type_message}')

    def should_have_correct_balance_background(self, is_positive: bool = True) -> None:
        balance_type_message = 'положительного' if is_positive else 'отрицательного'
        message = f'Проверить: блок {balance_type_message} баланса имеет верный фоновый цвет'
        with allure.step(message):
            balance_block = Block(self.page, self.balance_block, 'Балансы')
            if os.getenv('ENV_NAME') == 'prodlike':
                balance_block.should_have_background_color(BALANCE_BLOCK_BACKGROUND_WHITE)
            else:
                if is_positive:
                    balance_block.should_have_background_color(BALANCE_POSITIVE_BLOCK_BACKGROUND_YELLOW)
                else:
                    balance_block.should_have_background_color(BALANCE_NEGATIVE_BLOCK_BACKGROUND_RED)
