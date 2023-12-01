import re
import allure
from lib.helpers.url_helper import quote_url
from playwright.sync_api import Page, expect
from pom.pages.base_page import BasePage
from pom.page_factory.input import Input
from pom.page_factory.button import Button
import pom.pages.elk.main.page as elk

_ERROR_MESSAGE = ':Логин и\\или пароль указаны неверно'


class IdentityErrorPage(BasePage):
    def __init__(self, page: Page, signin: str = None) -> None:
        super().__init__(page,
                         base_url='https://identity.beeline.ru',
                         path='/identity/login',
                         query_params={
                             'signin': signin if signin else '',
                             'errorMessage': quote_url(_ERROR_MESSAGE)
                         },
                         name='Вход в Мой Билайн')
        self.signin = signin
        self.page = page

        self._container = self.page.locator('.content-wrap')

        self._auth_form = self._container.locator('[name=authForm]')
        self.login_input = Input(self.page, self._auth_form.locator('[name=userName]'), 'Логин')
        self.password_input = Input(self.page, self._auth_form.locator('[name=password]'), 'Пароль')
        self.signin_button = Button(self.page, self._auth_form.locator('.button'), 'Войти')

    def login(self, ctn: str, password: str):
        message = f'Авторизоваться пользователем {ctn} с постоянным паролем "{password}"'
        with allure.step(message):
            self.login_input.should_have_value(ctn)
            self.password_input.should_have_attribute('type', 'password')
            self.password_input.fill(password)
            self.signin_button.click()
            page = elk.ElkPage(self.page)
            page.should_have_correct_url()
            return page

    def should_have_correct_url(self):
        with allure.step(f'Проверить: {self.type_of} "{self.name}" открыта – адрес в браузере верный: {self._page_url}'):
            if self.signin:
                super().should_have_correct_url()
            else:
                pattern = re.compile(r"^https://identity\.beeline\.ru/identity/login\?signin=["
                                     r"a-z0-9]+&errorMessage=authError%3A%D0%9B%D0%BE%D0%B3%D0%B8%D0%BD\+%D0%B8%5C%D0"
                                     r"%B8%D0%BB%D0%B8\+%D0%BF%D0%B0%D1%80%D0%BE%D0%BB%D1%8C\+%D1%83%D0%BA%D0%B0%D0"
                                     r"%B7%D0%B0%D0%BD%D1%8B\+%D0%BD%D0%B5%D0%B2%D0%B5%D1%80%D0%BD%D0%BE$",
                                     re.IGNORECASE)
                expect(self.page).to_have_url(pattern)
