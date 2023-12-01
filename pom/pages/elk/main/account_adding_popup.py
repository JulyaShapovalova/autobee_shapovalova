import allure
from playwright.sync_api import Page, Locator
from pom.page_factory.button import Button
from pom.page_factory.description import Description
from pom.page_factory.input import Input
from pom.page_factory.tab import Tab
from pom.shared_components.modal import Modal


class AccountAddingPopup(Modal):
    def __init__(self, page: Page, parent_locator: Locator = None) -> None:
        super().__init__(page, 'Добавить аккаунт', parent_locator)
        self.page = page

        self.tab_login_password = Tab(self.page, self._tabs_form.locator('xpath=.//*[@data-component="Tab"][.//*[text()="Логин и пароль"]]'), 'Логин и пароль')
        self.tab_login = Tab(self.page, self._tabs_form.locator('xpath=.//*[@data-component="Tab"][.//*[text()="Логин"]]'), 'Логин')

        self._login_container = self._main_form.locator('xpath=.//*[@data-component="Input"][.//*[text()="Логин"]]')
        self.login_input = Input(self.page, self._login_container.locator('input'), 'Логин')
        self.login_input_hint = Description(self.page, self._login_container.locator('xpath=./*').nth(1), 'Валидационная подсказка')

        self._password_container = self._main_form.locator('xpath=.//*[@data-component="Input"][.//*[text()="Пароль"]]')
        self.password_input = Input(self.page, self._password_container.locator('input'), 'Пароль')

        self.add_account_button = Button(self.page, self._container.locator('[type=submit]'), 'Добавить')

        self.title_message = Description(self.page, self._container.locator('[data-component=Text]').first, 'Главное сообщение')
        self.subtitle_message = Description(self.page, self._container.locator('[data-component=Text]').nth(1), 'Сообщение')

    def add_account(self, ctn: str, password: str = None) -> None:
        with allure.step(f'Добавить аккаунт: {ctn}'):
            self.tab_login_password.should_be_selected()
            self.add_account_button.should_be_disabled()
            if not password:
                self.tab_login.click()
            self.login_input.fill(ctn)
            if password:
                self.password_input.fill(password)
            self.add_account_button.click()

    def should_have_title_message(self, message) -> None:
        with allure.step(f'Проверить: заглавное сообщение о добавлении пользователя верное: "{message}"'):
            self.title_message.should_have_text(message)

    def should_have_subtitle_message(self, message) -> None:
        with allure.step(f'Проверить: сообщение о добавлении пользователя верное: "{message}"'):
            self.subtitle_message.should_have_text(message)

    def should_have_login_validation_hint(self, hint) -> None:
        with allure.step(f'Проверить: текст подсказки валидации верный: "{hint}"'):
            self.login_input_hint.should_have_text(hint)